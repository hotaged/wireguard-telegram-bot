from bot.handlers.misc import dp, bot
from bot.handlers.filters import AdminLoginMessageFilter
from bot.db.models import TelegramUser
from bot.keyboards.base import BaseKeyboard
from bot.resources.strings import BASE_HANDLER_TEXT
from aiogram.types import Message


@dp.message_handler(commands=['start'])
async def start_message(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_id)

    return await bot.send_message(
        message.chat.id, BASE_HANDLER_TEXT,
        reply_markup=BaseKeyboard(user.is_admin)
    )


@dp.message_handler(AdminLoginMessageFilter())
async def admin_login_message(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_user, is_admin=True)
    await user.update_from_dict({'is_admin': True}).save()
    return await bot.send_message(
        message.chat.id, 'You are an admin now!',
        reply_markup=BaseKeyboard(user.is_admin)
    )


@dp.message_handler()
async def any_message_handler(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_id)

    return await bot.send_message(
        message.chat.id, BASE_HANDLER_TEXT,
        reply_markup=BaseKeyboard(user.is_admin)
    )