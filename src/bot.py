
import httpx
from urllib.parse import urljoin


from common.globals.log import logger
from api import ENDPOINT, User
from setting.configuration import BOT_ID, BOT_NAME, BOT_TOKEN
from connection import (
    Connection
)


class Bot:
    """记录机器人基本信息类"""

    def __init__(self, protocol, token):
        """
        Description:
            初始化bot 根据使用协议和token决定连接的对象
        Args:
            protocol (Any): bot 使用的监听协议
            token (str): bot token
        """
        self.connection = protocol
        self.__token = token
        self.me()

    def me(self):
        """  
        Description:
            查询服务端Bot信息
        """
        headers = {"Authorization": f"Bot {self.__token}"}
        result = httpx.get(urljoin(ENDPOINT, User.ME), headers=headers)
        result = result.json()
        logger.info(result)
        self.__bot_id = result["data"]["id"]
        self.__bot_name = result["data"]["username"]


bot = Bot("...", BOT_TOKEN)

print(bot.me())
