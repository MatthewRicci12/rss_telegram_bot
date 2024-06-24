from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
from rss_parser import RSSParser
from requests import get, Session
from requests_file import FileAdapter
import asyncio
import logging

LOGGER = logging.getLogger(__file__)


PREQUEL_FEED_URL = "https://www.prequeladventure.com/feed/"
TEST_FEED_URL = "https://lorem-rss.herokuapp.com/feed?unit=minute&interval=1"


class PrequelBot:
    """Contains all the logic for this bot"""
    def __init__(self: PrequelBot, underlying_bot: Bot):
        self.underlying_bot = underlying_bot
        self.num_rss_items = None

    async def send_start_message(self: PrequelBot, message: Message):
        await message.answer("Hey Aloe~ I'll keep an eye on those RSS updates, okay babe? ^_^")


    async def begin_listening(self, message: Message):
        while True:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.poll_feed(message, PREQUEL_FEED_URL))
                tg.create_task(self.poll_feed(message, TEST_FEED_URL))
            asyncio.sleep(30)
    
    async def poll_feed(self: PrequelBot, message: Message, rss_url: str):
            if not self.num_rss_items:
                self.num_rss_items = self.get_num_of_rss_items(rss_url)
            num_of_rss_items = self.get_num_of_rss_items(rss_url)

            if num_of_rss_items > self.num_rss_items:
                 await message.answer("There's been an update!")
                 self.num_rss_items = num_of_rss_items
            else:
                 await message.answer("Nothing new!")

    '''
    '''
            
    def get_num_of_rss_items(self, rss_url: str):
        session = Session()
        response = session.get(rss_url)

        rss = RSSParser.parse(response.text)

        return len(rss.channel.items)
