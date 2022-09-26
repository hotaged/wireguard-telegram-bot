from aiogram import filters, types
from tortoise.exceptions import DoesNotExist

from bot.settings import token
from bot.db.models import TelegramUser


class AdminLoginMessageFilter(filters.Filter):
    async def check(self, message: types.Message) -> bool:
        return f'/op {token}' == message.text


class IsAdminUserQueryFilter(filters.Filter):
    async def check(self, query: types.CallbackQuery) -> bool:
        try:
            user = await TelegramUser.get(telegram_id=query.from_user.id)
            return user.is_admin
        except DoesNotExist:
            return False
