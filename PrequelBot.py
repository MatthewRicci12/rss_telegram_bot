from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
from collections import namedtuple
import os
from rss_parser import RSSParser
from requests import get, Session
from requests_file import FileAdapter
from typing import List

import asyncio
import json
import logging

LOGGER = logging.getLogger(__file__)


PREQUEL_FEED_URL = "https://www.prequeladventure.com/feed/"
TEST_FEED_URL = "http://localhost/mock.xml"
CHATS_FILE_NAME = "chats.json"

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

class PrequelBot:
    def __init__(self: PrequelBot, underlying_bot: Bot):
        self.underlying_bot = underlying_bot
        self.feeds = {}
        self.load_feeds()

    async def send_start_message(self: PrequelBot, chat_id: int):
        await self.underlying_bot.send_message(chat_id, "Hey Aloe~ I'll keep an eye on those RSS updates, okay babe? ^_^")

    def chat_already_registered(self, chats, chat_id):
        if len(chats[0]) == 0:
            return False

        for cur_chat in chats:
            cur_chat_id = int(cur_chat.split()[0])
            if chat_id == cur_chat_id:
                return True
        return False
    
    def serialize_feeds(self, fh):
        import copy

        feeds_copy = copy.deepcopy(self.feeds)

        for chat_id in feeds_copy.keys():
            feeds = feeds_copy[chat_id]
            for i in range(len(feeds)):
                feeds[i] = feeds[i].__dict__
        
        json.dump(feeds_copy, fh)

    async def register_chat(self, chat_id):
        lock = asyncio.Lock()
        async with lock:
            if str(chat_id) in self.feeds:
                return
            with open(CHATS_FILE_NAME, "w") as fh:
                self.feeds[chat_id] = [Feed("Prequel", PREQUEL_FEED_URL), Feed("Test", TEST_FEED_URL)]
                self.serialize_feeds(fh)

                
    def load_feeds(self):
        with open(CHATS_FILE_NAME, "r") as fh:
            try:
                decoded_feeds = json.load(fh)
                for chat_id, list_of_feeds in decoded_feeds.items():
                    cur_feeds_list = []
                    for feed_dict in list_of_feeds:
                        cur_feeds_list.append(Feed(feed_dict["name"], feed_dict["url"]))
                    self.feeds[chat_id] = cur_feeds_list

            except json.JSONDecodeError as e:
                print(e.msg)
                 

    async def begin_listening(self):
        while True:
            async with asyncio.TaskGroup() as tg:
                for chat_id in self.feeds.keys():
                    tg.create_task(self.poll_feeds(chat_id))
            await asyncio.sleep(10)
    
    async def poll_feeds(self: PrequelBot, chat_id: int):
            feed_list = self.feeds[chat_id]

            for feed in feed_list:
                cur_num_of_rss_items = feed.get_num_of_rss_items()

                if cur_num_of_rss_items > feed.num_items:
                    await self.underlying_bot.send_message(chat_id, f"There's been an update to your {feed.name} feed!")
                    feed.num_items = cur_num_of_rss_items
                else:
                    await self.underlying_bot.send_message(chat_id, f"Nothing new from your {feed.name} feed!")


    

class Feed:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.num_items = self.get_num_of_rss_items()

    def get_num_of_rss_items(self):

        session = Session()

        if (self.name == "Test"):
            response = session.get(self.url, verify=False)
        else:
            response = session.get(self.url)

        rss = RSSParser.parse(response.text)

        return len(rss.channel.items)