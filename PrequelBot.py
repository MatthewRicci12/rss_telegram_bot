from __future__ import annotations

from aiogram import Bot
from aiogram.types import Message
import logging

LOGGER = logging.getLogger(__file__)


class PrequelBot:
    """Contains all the logic for this bot"""
    def __init__(self: PrequelBot, underlying_bot: Bot):
        self.underlying_bot = underlying_bot

    async def send_message(self: PrequelBot, message: Message):
        await message.answer('Hello from my router!')



