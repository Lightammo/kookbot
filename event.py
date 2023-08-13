from enum import Enum
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


class Sign:
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
        if self.sign == Sign.EVENT:
            return f"[Event]This is a event data:{self.data}"

        if self.sign == Sign.HELLO:
            return "[Websocket] bot connectted."

        if self.sign == Sign.PONG:
            return "[heartbeats] pong"

        """ 重连未装载
        1 重新获取 gateway;
        2 清空本地的 sn 计数;
        3 清空本地消息队列.
        """

        if self.sign == Sign.RESUME:
            return "[Error Msg] RESUME"

        if self.sign == Sign.RECONNECT:
            return "[Error Msg] RECONNECT"

        if self.sign == Sign.RESUME_ACK:
            return "[Error Msg] RESUME_ACK"


class Event(metaclass=ABCMeta):
    def __init__(self):
        ...

    def load(self, data):
        self.channel_type = data.get("channel_type", "")
        self.type = data.get("type", 0)
        self.target_id = data.get("target_id", "")
        self.author_id = data.get("author_id", "")
        self.content = data.get("content", "")
        self.msg_id = data.get("msg_id", "")
        self.msg_timestamp = data.get("msg_timestamp", "")
        self.extra = data.get("extra", {})
        self.nonce = data.get("nonce", "")
        # docs not supported.
        self.from_type = data.get("from_type", 0)

    def get_user_message(self):
        ...
