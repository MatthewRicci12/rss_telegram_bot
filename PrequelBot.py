from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
from rss_parser import RSSParser
from requests import get, Session
from requests_file import FileAdapter
import logging

LOGGER = logging.getLogger(__file__)




class PrequelBot:
    """Contains all the logic for this bot"""
    def __init__(self: PrequelBot, underlying_bot: Bot):
        self.underlying_bot = underlying_bot
        self.num_rss_items = None

    async def send_start_message(self: PrequelBot, message: Message):
        user = message.from_user.username
        await message.answer("Hey Aloe~ I'll keep an eye on those RSS updates, okay babe? ^_^")


    async def poll_feed(self: PrequelBot, message: Message):
            if not self.num_rss_items:
                self.initial_read_rss()
            num_of_rss_items = self.get_num_of_rss_items()

            if num_of_rss_items > self.num_rss_items:
                 await message.answer("There's been an update!")
                 self.num_rss_items = num_of_rss_items
            else:
                 await message.answer("Nothing new!")

    '''
    '''
            
    def get_num_of_rss_items(self):
        rss_url = "file:///Users/matth/Coding/Python/rss_telegram_bot/mock_rss/mock.xml"
        session = Session()
        session.mount("file://", FileAdapter())
        response = session.get(rss_url)

        rss = RSSParser.parse(response.text)

        return len(rss.channel.items)

    def initial_read_rss(self):
        #For testing purposes
        self.num_rss_items = self.get_num_of_rss_items()

