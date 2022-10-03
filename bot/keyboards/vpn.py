import typing

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from bot.utils import unique_query_id


QUERY_GET_PEER = unique_query_id()


class ListAvailableServersKeyboard(InlineKeyboardMarkup):
    def __init__(self, items: typing.List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        map(
            lambda x: self.add(
                InlineKeyboardButton(
                    x, callback_data=f'{QUERY_GET_PEER}.{x}'
                )
            ),
            items
        )

    @classmethod
    def query_get_peer(cls, callback_query: CallbackQuery) -> bool:
        return callback_query.data.startswith(QUERY_GET_PEER)


class VPNKeyboard(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)