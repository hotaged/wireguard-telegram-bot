from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)

from bot.db.models import WireguardServer
from bot.handlers.misc import (
    dp,
    bot
)

from bot.handlers.filters import IsAdminUserQueryFilter
from bot.keyboards.servers import (
    AdminServerKeyboard,
    AdminListKeyboard
)
from bot.keyboards.base import BaseKeyboard

from bot.resources.strings import (
    SERVER_MENU_TEXT,
    SERVER_ADD_WEBHOOK,
    SERVER_ADD_SECRET,
    SERVER_ADD_FAILED,
    SERVER_ADD_COUNTRY,
    SERVER_ADD_SUCCESS,
    BASE_HANDLER_TEXT,
    SERVER_LIST_TEXT
)


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    BaseKeyboard.query_servers
)
async def callback_query_servers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    return await bot.edit_message_text(
        SERVER_MENU_TEXT,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

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


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    AdminServerKeyboard.query_list
)
async def callback_query_list_servers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    content = await WireguardServer.as_list_items()

    offset, limit = AdminListKeyboard.parse_callback_query(callback_query)

    await bot.edit_message_text(
        SERVER_LIST_TEXT,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

        reply_markup=AdminListKeyboard(content, offset, limit)
    )


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    AdminListKeyboard.query_back
)
async def callback_query_list_back(callback_query: types.CallbackQuery):
    await callback_query_servers(callback_query)


@dp.callback_query_handler(
    IsAdminUserQueryFilter(),
    AdminServerKeyboard.query_back
)
async def callback_query_back_default(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    return await bot.edit_message_text(
        BASE_HANDLER_TEXT,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

        reply_markup=BaseKeyboard(True)
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
async def process_secret(message: types.Message, state: FSMContext):
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
async def process_country(message: types.Message, state: FSMContext):
    async with state.proxy() as context:
        context['country'] = message.text

        wg_server = await WireguardServer.create(
            webhook_url=context['webhook'],
            server_key=context['secret'],
            country=context['country']
        )

        await wg_server.download_peers()

    await bot.send_message(
        message.chat.id, SERVER_ADD_SUCCESS
    )

    await bot.send_message(
        message.chat.id, SERVER_MENU_TEXT,
        reply_markup=AdminServerKeyboard()
    )
    await state.finish()

