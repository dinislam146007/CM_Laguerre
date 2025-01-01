import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from basic.handlers import router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from parser.parser import run_task
from queue import Queue

API_TOKEN = '6742138204:AAGV2ajZM8WQ6scFZgxbV0z_ZaQwxO5YaC0'
SIGNAL_QUEUE = Queue()  # Очередь для сигналов из парсера

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, session=AiohttpSession(), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def on_startup():
    logging.info("Бот запущен")


async def on_shutdown():
    await dp.storage.close()
    await bot.close()
    logging.info("Бот остановлен")


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def notify_signals():
    """
    Асинхронный обработчик сигналов из очереди.
    """
    while True:
        if not SIGNAL_QUEUE.empty():
            signal = SIGNAL_QUEUE.get()
            message = f"Новый сигнал:\nИнструмент: {signal['symbol']}\nИнтервал: {signal['interval']}\nСигнал: {signal['flag']}"
            await bot.send_message(chat_id=6634277726, text=message)
        await asyncio.sleep(1)


async def main():
    # Запуск парсера в отдельном потоке
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run_task, ['1D', '4H', '1H', '30'], SIGNAL_QUEUE)

    # Запуск бота
    asyncio.create_task(notify_signals())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
