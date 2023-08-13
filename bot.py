

from configuration import BOT_ID, BOT_NAME, BOT_TOKEN
from connection import (
    Connection
)


class Bot:
    def __init__(self):
        self.conn = Connection()

    def setup(self):
        self.conn.setup()
