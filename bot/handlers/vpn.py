from aiogram import types

from bot.db.models import (
    TelegramUser,
    WireguardServer
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
    VPN_LIST_SERVERS
)


@dp.callback_query_handler(BaseKeyboard.query_vpn)
async def callback_query_vpn(message: types.Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_id)

    countries = await WireguardServer.list_countries()

    if not await user.wg_peers.all().count():
        return await bot.send_message(
            message.chat.id, VPN_LIST_SERVERS,
            reply_markup=ListAvailableServersKeyboard(countries)
        )

