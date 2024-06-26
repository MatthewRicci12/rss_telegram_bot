from __future__ import annotations

import logging

from dotenv import dotenv_values

from aiogram import Bot, Router, Dispatcher
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.error_event import ErrorEvent
from aiogram.filters import CommandStart, Command

import PrequelBot

LOGGER = logging.getLogger(__file__)
config = dotenv_values(".env")

DEBUGGING = True if config["DEBUGGING"].lower() == "true" else False
TOKEN = config["TOKEN"]


tgbot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
prequel_bot = PrequelBot.PrequelBot(tgbot)
router = Router()
dispatcher = Dispatcher()
dispatcher.include_router(router)


if not DEBUGGING:

    @router.error(F.update.message.as_("message"))
    async def error(event: ErrorEvent, message: Message) -> None:
        """Catches all errors"""
        LOGGER.critical(
            "An error occurred from this message: %s",
            message.text
        )
        LOGGER.critical("error was this: %s", str(event.exception))
    


@router.message(CommandStart())
async def start_handler(message: Message):
    chat_id = message.chat.id
    await prequel_bot.register_chat(chat_id)
    await prequel_bot.send_start_message(chat_id)