from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.handlers.misc import dp, bot
from bot.handlers.filters import IsAdminUserQueryFilter
from bot.keyboards.servers import AdminServerKeyboard
from bot.keyboards.base import BaseKeyboard
from bot.resources.strings import (
    SERVER_MENU_TEXT,
    SERVER_ADD_WEBHOOK,
    SERVER_ADD_SECRET,
    SERVER_ADD_FAILED,
    SERVER_ADD_COUNTRY,
    SERVER_ADD_SUCCESS
)
from aiogram import types


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


class AddStorageForm(StatesGroup):
    webhook = State()
    secret = State()
    country = State()


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    AdminServerKeyboard.query_add
)
async def callback_query_add_server(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await AddStorageForm.webhook.set()
    return await bot.send_message(
        callback_query.message.chat.id,
        SERVER_ADD_WEBHOOK
    )


@dp.message_handler(
    IsAdminUserQueryFilter(),
    state=AddStorageForm.webhook
)
async def process_webhook(message: types.Message, state: FSMContext):
    async with state.proxy() as context:
        context['webhook'] = message.text

    await AddStorageForm.next()
    return await bot.send_message(
        message.chat.id, SERVER_ADD_SECRET
    )


@dp.message_handler(
    IsAdminUserQueryFilter(),
    state=AddStorageForm.secret
)
async def process_webhook(message: types.Message, state: FSMContext):
    async with state.proxy() as context:
        context['secret'] = message.text

    await AddStorageForm.next()
    return await bot.send_message(
        message.chat.id, SERVER_ADD_COUNTRY
    )


@dp.message_handler(
    IsAdminUserQueryFilter(),
    state=AddStorageForm.country
)
async def process_webhook(message: types.Message, state: FSMContext):
    async with state.proxy() as context:
        context['country'] = message.text

    await state.finish()
