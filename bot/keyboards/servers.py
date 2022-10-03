import typing

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from bot.keyboards.base import ListItem
from bot.resources.strings import (
    BUTTON_LIST,
    BUTTON_BACK,
    BUTTON_ADD
)
from bot.utils import unique_query_id

QUERY_BACK = unique_query_id()
QUERY_LIST = unique_query_id()
QUERY_ADD = unique_query_id()

QUERY_LIST_BACK = unique_query_id()
QUERY_LIST_AT = unique_query_id()


class AdminServerKeyboard(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        kwargs.update({'row_width': 1})
        super().__init__(*args, **kwargs)

        self.add(
            InlineKeyboardButton(
                BUTTON_LIST,
                callback_data=f'{QUERY_LIST}.0-5'
            ),
            InlineKeyboardButton(
                BUTTON_ADD,
                callback_data=QUERY_ADD
            ),
            InlineKeyboardButton(
                BUTTON_BACK,
                callback_data=QUERY_BACK
            ),
        )

    @classmethod
    def query_list(cls, query: CallbackQuery) -> bool:
        return query.data.startswith(f'{QUERY_LIST}.')

    @classmethod
    def query_back(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_BACK

    @classmethod
    def query_add(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_ADD


class AdminListKeyboard(InlineKeyboardMarkup):
    def __init__(self, items: ListItem, offset: int = 0, limit: int = 3, *args, **kwargs):
        super().__init__(*args, **kwargs)

        docstring = f'{offset} - {offset + limit} of {len(items)}'

        for item in items[offset:offset + limit]:
            self.add(InlineKeyboardButton(
                item[0], callback_data=f'{QUERY_LIST_AT}.{item[1]}'
            ))

        if offset < limit:
            previous_text = '.'
            previous_query = '*'
        else:
            previous_text = '<'
            previous_query = f'{QUERY_LIST}.{offset - limit}-{limit}'

        if offset + limit >= len(items) - 1:
            next_text = '.'
            next_query = '*'
        else:
            next_text = '>'
            next_query = f'{QUERY_LIST}.{offset + limit}-{limit}'

        self.row(
            InlineKeyboardButton(
                previous_text,
                callback_data=previous_query
            ),
            InlineKeyboardButton(
                docstring,
                callback_data='*'
            ),
            InlineKeyboardButton(
                next_text,
                callback_data=next_query
            ),
        )
        self.add(
            InlineKeyboardButton(
                BUTTON_BACK,
                callback_data=QUERY_LIST_BACK
            ),
        )

    @classmethod
    def query_back(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_LIST_BACK

    @classmethod
    def parse_callback_query(cls, callback_query: CallbackQuery) -> typing.Tuple[int, int]:
        offset, limit = tuple(map(int, callback_query.data.split('.')[-1].split('-')))
        return offset, limit
