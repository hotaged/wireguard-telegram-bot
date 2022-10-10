from aiogram import types
from typing import Coroutine

from aiohttp.client_exceptions import (
    ClientConnectionError
)

from bot.db.models import (
    TelegramUser,
    WireguardServer,
    WireguardPeer
)
from bot.handlers.default import (
    start_message
)
from bot.handlers.misc import (
    bot, dp
)
from bot.keyboards.base import (
    BaseKeyboard
)
from bot.keyboards.vpn import (
    ListAvailableServersKeyboard
)
from bot.resources.strings import (
    VPN_LIST_SERVERS, WAIT,
    VPN_SERVER_UNAVAILABLE
)


async def send_qrcode_and_config(
        peer: WireguardPeer,
        chat_id: int,
        on_success: Coroutine = None,
        on_failure: Coroutine = None
):
    try:
        config, qrcode = await peer.config_and_qrcode()
    except ClientConnectionError:

        if on_failure:
            await on_failure

        return await bot.send_message(chat_id, VPN_SERVER_UNAVAILABLE)

    if on_success:
        await on_success

    await bot.send_message(
        chat_id, config
    )

    await bot.send_photo(
        chat_id, qrcode
    )

    return


@dp.callback_query_handler(BaseKeyboard.query_vpn)
async def callback_query_vpn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user, _ = await TelegramUser.get_or_create(telegram_id=callback_query.message.from_id)
    countries = await WireguardServer.list_countries()

    if not await user.wg_peers.all().count():
        return await bot.send_message(
            callback_query.message.chat.id, VPN_LIST_SERVERS,
            reply_markup=ListAvailableServersKeyboard(countries)
        )

    await send_qrcode_and_config(
        await user.wg_peers.all().first(),
        callback_query.message.chat.id
    )


@dp.callback_query_handler(ListAvailableServersKeyboard.query_get_peer)
async def callback_query_get_peer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    message = await bot.send_message(
        callback_query.message.chat.id, WAIT
    )

    _, country = callback_query.data.split('.')

    available_server = await WireguardServer.get_by_country(country)

    if not available_server:
        return await bot.edit_message_text(
            VPN_SERVER_UNAVAILABLE,
            callback_query.message.chat.id,
            message.message_id
        )

    peer = await available_server.available_peers().first()
    user, _ = await TelegramUser.get_or_create(telegram_id=callback_query.message.from_id)

    async def on_success():
        peer.tg_user = user
        await peer.save()
        await message.delete()

    async def on_failure():
        await message.delete()

    await send_qrcode_and_config(
        peer,
        callback_query.message.chat.id,
        on_success(), on_failure()
    )



