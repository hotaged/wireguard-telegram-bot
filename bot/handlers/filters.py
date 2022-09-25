from aiogram import filters, types
from bot.settings import token


class AdminLoginMessageFilter(filters.Filter):
    async def check(self, message: types.Message) -> bool:
        return f'/op {token}' == message.text
