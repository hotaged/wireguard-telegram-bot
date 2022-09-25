import logging

from bot import settings, db
from bot.handlers.misc import dp
from aiogram.utils import executor

if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


async def on_startup(*_):
    await db.init()


async def on_shutdown(*_):
    await db.shutdown()


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
