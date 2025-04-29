from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from bot.core.config import settings

app = web.Application()

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


DEBUG = settings.DEBUG
