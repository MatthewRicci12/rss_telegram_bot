from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
from collections import namedtuple
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
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

class PrequelBot:
    """Contains all the logic for this bot"""
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
    
    async def register_chat(self, chat_id):
        lock = asyncio.Lock()
        async with lock:
            with open(CHATS_FILE_NAME, "r+") as fh:
                try:
                    chats_to_feeds = json.load(fh)
                    if chat_id in chats_to_feeds:
                        return
                    json.dump({chat_id : {"Prequel" : PREQUEL_FEED_URL, "Test" : TEST_FEED_URL}}, fh)
                except json.JSONDecodeError:
                    json.dump({chat_id : {"Prequel" : PREQUEL_FEED_URL, "Test" : TEST_FEED_URL}}, fh)

                
    def load_feeds(self):
        with open(CHATS_FILE_NAME, "r") as fh:
            try:
                chats_to_feeds = json.load(fh)
                x = 3
            except json.JSONDecodeError:
                return
            # chat_info = fh.read()
            # if not chat_info:
            #     return
            # chat_info = chat_info.split("\n\n")

            # for chat_info_packet in chat_info:
            #     split_chat_info_packet = chat_info_packet.split()
            #     cur_chat_id = split_chat_info_packet[0]
            #     cur_chat_feeds = []

            #     for feed_name, feed_url in pairwise(split_chat_info_packet[1:]):
            #         cur_feed = Feed(feed_name, feed_url)
            #         cur_chat_feeds.append(cur_feed)

            #     self.feeds[cur_chat_id] = cur_chat_feeds

                 

    async def begin_listening(self):
        while True:
            async with asyncio.TaskGroup() as tg:
                for cur_chat_id, feeds in self.feeds.items():
                    tg.create_task(self.poll_feeds(cur_chat_id, feeds))
            await asyncio.sleep(30)
    
    async def poll_feeds(self: PrequelBot, chat_id: int, feeds: List[Feed]):
            for feed in feeds:
                cur_num_of_rss_items = self.get_num_of_rss_items(feed)

                if not feed.num_items:
                    feed.num_items = self.get_num_of_rss_items(feed)

                if cur_num_of_rss_items > feed.num_items:
                    await self.underlying_bot.send_message(chat_id, f"There's been an update to your {feed.name} feed!")
                    feed.num_items = cur_num_of_rss_items
                else:
                    await self.underlying_bot.send_message(chat_id, f"Nothing new from your {feed.name} feed!")

    def get_num_of_rss_items(self, feed: Feed):

        session = Session()


        if (feed.name == "Test"):
            print("TEST")
            response = session.get(feed.url, verify=False)
        else:
            response = session.get(feed.url)

        rss = RSSParser.parse(response.text)

        return len(rss.channel.items)
    


class Feed:
    def __init__(self, name, url):
         self.name = name
         self.url = url
         self.num_items = None