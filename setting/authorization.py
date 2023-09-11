import os
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


class BaseTokenFetcher(metaclass=ABCMeta):
    @abstractmethod
    def get_token(self):
        ...


class BaseToken(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name):
        ...

    @property
    @abstractmethod
    def token(self):
        ...

    @token.setter
    @abstractmethod
    def token(self):
        ...


class TokenFetcher(BaseTokenFetcher):
    def __init__(self):
        ...

    def get_token(self):
        return os.getenv("BOT_TOKEN", "")


class Token(BaseToken):
    def __init__(self, name, token_fetcher: BaseTokenFetcher,  expired_limit=timedelta(days=1)):
        """_summary_

        Args:
            name (_type_): _description_
            token_fetcher (TokenFetcher): _description_
            expired_limit (timedelta): _description_. Defaults to timedelta(days=1).
        """
        self.__name = name
        self.__expired_limit = expired_limit

        self.token_fetcher = token_fetcher
        self.__token = self.token_fetcher.get_token()
        self.__expired_time: datetime = None

    def info(self):
        return self.__name

    @property
    def token(self):
        self.refresh_token()
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token
        self.__expired_time = datetime.now()

    def refresh_token(self):
        """刷新token"""
        if self.is_expired:
            self.token = self.token_fetcher.get_token()

    def is_expired(self) -> bool:
        """判断token是否超时"""
        if datetime.now() - self.__expired_time >= self.__expired_limit:
            return True
        return False


if __name__ == "__main__":

    t = Token(name="bot_token", token_fetcher=TokenFetcher())
    print(t.token)
