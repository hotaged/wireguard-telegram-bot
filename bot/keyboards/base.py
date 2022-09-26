from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery,
)
from bot.resources.strings import (
    BUTTON_GET_VPN,
    BUTTON_SERVERS
)
from bot.utils import unique_query_id


QUERY_VPN = unique_query_id()
QUERY_SERVERS = unique_query_id()


class BaseKeyboard(InlineKeyboardMarkup):
    def __init__(self, is_admin: bool, *args, **kwargs):
        self.is_admin = is_admin

        kwargs.update({'row_width': 1})
        super().__init__(*args, **kwargs)

        self.add(
            InlineKeyboardButton(
                BUTTON_GET_VPN,
                callback_data=QUERY_VPN
            )
        )

        if self.is_admin:
            self.add(
                InlineKeyboardButton(
                    BUTTON_SERVERS,
                    callback_data=QUERY_SERVERS
                )
            )

    @classmethod
    def query_vpn(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_VPN

    @classmethod
    def query_servers(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_SERVERS
