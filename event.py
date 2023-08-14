import requests
import json
from urllib.parse import urljoin
from dataclasses import dataclass, asdict

from enum import Enum, IntEnum, StrEnum
from dataclasses import dataclass
from setting.configuration import BOT_TOKEN
from api import ENDPOINT, Message, User

ID = None


class SignalType(IntEnum):
    """"""
    EVENT = 0
    HELLO = 1
    PING = 2
    PONG = 3
    RESUME = 4
    RECONNECT = 5
    RESUME_ACK = 6


class Signaling:
    """websocket 信令解析"""

    def __init__(self):
        self.sign = None
        self.data = {}
        self.session_num = None

    def load(self, sign):
        self.sign = sign.get("s")
        self.data = sign.get("d")
        self.session_num = sign.get("sn")

    def to_event(self):
        """_summary_

        Returns:
            typle: sign_type, sign_data
        """
        if self.sign == SignalType.EVENT:
            event = Event()
            event.load(self.data)
            # 应过滤自己的发言
            global ID
            if not ID:
                ID = Action().me()
            if event.author_id != ID:
                Action().echo(event.target_id, event.content)
            return f"[Event]This is a event sender:{event.target_id}, msg:{event.content}"

        if self.sign == SignalType.HELLO:
            return "[Websocket] bot connectted."

        if self.sign == SignalType.PONG:
            return "[heartbeats] pong"

        """ 重连未装载
        1 重新获取 gateway;
        2 清空本地的 sn 计数;
        3 清空本地消息队列.
        """

        if self.sign == SignalType.RESUME:
            return "[Error Msg] RESUME"

        if self.sign == SignalType.RECONNECT:
            return "[Error Msg] RECONNECT"

        if self.sign == SignalType.RESUME_ACK:
            return "[Error Msg] RESUME_ACK"


class EventType(IntEnum):
    WORDS = 1  # 文字消息,
    PICTURE = 2  # 图片消息，
    VIDEO = 3  # 视频消息，
    FILE = 4  # 文件消息，
    VIOCE = 8  # 音频消息，
    KMD = 9  # KMarkdown，
    CARD = 10  # card 消息，
    SYS = 255  # 系统消息,


class Event:
    def __init__(self):
        self.channel_type: str = None
        self.type: int = None
        self.target_id: str = None
        self.author_id: str = None
        self.content: str = None
        self.msg_id: str = None
        self.msg_timestamp: int = None
        self.nonce: str = None
        self.extra = None

    def load(self, data):
        self.channel_type = data.get("channel_type", "")
        self.type = data.get("type", 0)
        self.target_id = data.get("target_id", "")
        self.author_id = data.get("author_id", "")
        self.content = data.get("content", "")
        self.msg_id = data.get("msg_id", "")
        self.msg_timestamp = data.get("msg_timestamp", "")
        self.nonce = data.get("nonce", "")
        self.extra = data.get("extra", {})
        # docs not supported.
        self.from_type = data.get("from_type", 0)

    def get_user_message(self):
        ...


def requestor(method, url, headers, **kwargs):
    """A requestor can catch exception."""
    result = {}
    try:
        response = requests.request(
            method=method, url=url, headers=headers, timeout=300, **kwargs)
        result = response.json()
    except json.decoder.JSONDecodeError as e:
        ...
        # l.warning(f"api: {method ,url}, {e}")
    except Exception as e:
        # logging.warning(f"api: {method ,url}, {e}")
        ...
    if result.get("code", -1) != 0:
        raise RuntimeError(f"url:{url}, param:{kwargs}")

    return result


class Action:
    def __init__(self):
        ...

    def me(self):
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        result = requestor("GET", urljoin(ENDPOINT, User.ME),
                           headers=headers)
        return result["data"]["id"]

    def echo(self, target_id, content):
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        body = {
            "target_id":  target_id,
            "content": content
        }
        requestor("POST", urljoin(ENDPOINT, Message.CREATE),
                  headers=headers, json=body)
        ...
