from bot.handlers.misc import dp, bot
from aiogram.types import Message


@dp.message_handler(commands=['start'])
async def start_message(message: Message):
    return await bot.send_message(message.chat.id, 'Hello!')


@dp.message_handler()
async def echo_message(message: Message):
    return await bot.send_message(message.chat.id, message.text)
