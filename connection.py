from threading import Thread
import time
import json
import logging
import asyncio
from queue import Queue
from enum import Enum
from urllib.parse import urljoin, urlparse, parse_qs


import requests
from websockets.sync.client import connect

from driver import Driver
from api import ENDPOINT, GATEWAY, Guild, Channel, Message
from common.globals.log import logger
from setting.configuration import BOT_TOKEN
from setting.setting import ENABLE_COMPRESS
from event import Signaling
from utils import bytes_to_str


SESSION_NUM = 0

SendQueue = Queue()
ReceiveQueue = Queue()


def requestor(method, url, headers, **kwargs):
    """A requestor can catch exception."""
    result = {}
    try:
        response = requests.request(
            method=method, url=url, headers=headers, timeout=300, **kwargs)
        result = response.json()
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"api: {method ,url}, {e}")
    except Exception as e:
        logging.warning(f"api: {method ,url}, {e}")
    if result.get("code", -1) != 0:
        ...

    return result


class Connection:
    """kook 链接服务端机器人的方法是通过websocket或webhook"""

    def __init__(self):
        # 维护线程JOB
        self.thread_list: list[Driver] = [
            Monitor,
            HeartBeats,
            SendConsumer,
            RecvConsumer
        ]

    def __call_gateway(self):
        """
        Descriptions:
            通过kook gateway获取wss链接地址
        Returns:
            str: websocket uri
        """
        params = {"compress": 1 if ENABLE_COMPRESS else 0}
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}

        result = requestor(
            "GET", urljoin(ENDPOINT, GATEWAY), params=params, headers=headers
        )
        self.ws_uri = result["data"]["url"]

        # get token.
        try:
            parsed = urlparse(self.ws_uri)._asdict()
            query = parse_qs(parsed.get("query"))
            self.token, = query["token"] if query else [""]
        except Exception as e:
            logger.exception(e)

        return self.ws_uri

    def setup(self):
        """启动反向连接"""
        # 构建链接
        self.connection = connect(self.__call_gateway())
        SendQueue.put("HELLO")

        # 启动任务线程
        for obj in self.thread_list:
            driver = obj(self.connection)
            driver.setup()

    def teardown(self):
        """关闭反向连接"""
        # 启动任务线程
        for obj in self.thread_list:
            driver = obj(self.connection)
            driver.teardown()


class Monitor(Driver):
    """监听线程"""

    def __init__(self, connection):
        super().__init__(connection)
        self.on_listen = False

    def setup(self):
        self.on_listen = True
        self.start_listener()

    def teardown(self):
        self.on_listen = False

    def start_listener(self):
        Thread(target=self.on_listening).start()

    def on_listening(self):
        """监听线程"""
        while self.on_listen:
            message = self.connection.recv()
            message = json.loads(message)
            ReceiveQueue.put(message)
            time.sleep(0.1)


class HeartBeats(Driver):
    """心跳线程"""

    def __init__(self, connection):
        super().__init__(connection)
        self.on_heartbeats = False

    def setup(self):
        self.on_heartbeats = True
        self.start_heartbeats()

    def teardown(self):
        self.on_heartbeats = False

    def start_heartbeats(self):
        Thread(target=self.__heartbeats).start()

    def __heartbeats(self):
        """心跳线程"""

        while self.on_heartbeats:
            logger.debug(f"now session num: {SESSION_NUM}")
            SendQueue.put(json.dumps({
                "s": 2,
                "sn": SESSION_NUM
            }))
            logger.info("[heartbeats] ping")
            time.sleep(25)


class SendConsumer(Driver):
    def __init__(self, connection):
        super().__init__(connection)
        self.on_consume = False

    def setup(self):
        self.on_consume = True
        self.start_consume_queue()

    def teardown(self):
        self.on_consume = False

    def start_consume_queue(self):
        Thread(target=self.consume_queue).start()

    def consume_queue(self):
        while self.on_consume:
            msg = SendQueue.get()
            self.connection.send(msg)


class RecvConsumer(Driver):
    def __init__(self, connection):
        super().__init__(connection)
        self.sign = Signaling()
        self.on_consume = False

    def setup(self):
        self.on_consume = True
        self.start_consume_queue()

    def teardown(self):
        self.on_consume = False

    def start_consume_queue(self):
        Thread(target=self.consume_queue).start()

    def consume_queue(self):
        while self.on_consume:
            sign = ReceiveQueue.get()
            self.sign.load(sign)
            if self.sign.session_num:
                global SESSION_NUM
                SESSION_NUM = self.sign.session_num
            event = self.sign.to_event()

            logger.info(event)


if __name__ == "__main__":
    conn = Connection()
    conn.setup()
