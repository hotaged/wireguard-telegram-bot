from bot.handlers.misc import dp, bot
from bot.handlers.filters import IsAdminUserQueryFilter
from bot.keyboards.servers import AdminServerKeyboard
from bot.keyboards.base import BaseKeyboard
from bot.resources.strings import SERVER_MENU_TEXT
from aiogram import types


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    AdminServerKeyboard.query_add
)
async def callback_query_add_server(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    return await bot.send_message(
        callback_query.message.chat.id, 'Adding server'
    )


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    BaseKeyboard.query_servers
)
async def callback_query_servers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    return await bot.send_message(
        callback_query.message.chat.id, SERVER_MENU_TEXT,
        reply_markup=AdminServerKeyboard()
    )