import asyncio
import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from basic.handlers import router
# from administrate.admin import router_admin
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from parser.parser import *


API_TOKEN = '6742138204:AAGV2ajZM8WQ6scFZgxbV0z_ZaQwxO5YaC0'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, session=AiohttpSession(), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)
# dp.include_router(router_admin)


async def on_startup():
    logging.info("Бот запущен")


async def on_shutdown():
    await dp.storage.close()
    await bot.close()
    logging.info("Бот остановлен")


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def main():
    await dp.start_polling(bot)
    await run_task(['1D', '4H', '1H', '30'], TRADINGVIEW_EMAIL, TR_LINK, bot)


if __name__ == "__main__":
    asyncio.run(main())
