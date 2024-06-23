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
from aiogram.filters import CommandStart

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
async def handler(message: Message):
    user = message.from_user.username
    if user != "AloeFerr":
        await message.answer("Oh, Alo- Oh wait, you're not Aloe. Sigh. Here's your payload:\n\n")
    else:
        await message.answer("Oh, Aloe!~ Hello babe, you're looking so handsome this evening. Thanks for checkin' in.~\n\nAnyways, here's that message payload:\n\n")
    await message.answer(f"{message}")