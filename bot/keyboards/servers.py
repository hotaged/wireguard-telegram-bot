from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from bot.resources.strings import (
    BUTTON_LIST,
    BUTTON_BACK,
    BUTTON_ADD
)
from bot.utils import unique_query_id


QUERY_BACK = unique_query_id()
QUERY_LIST = unique_query_id()
QUERY_ADD = unique_query_id()


class AdminServerKeyboard(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        kwargs.update({'row_width': 1})
        super().__init__(*args, **kwargs)

        self.add(
            InlineKeyboardButton(
                BUTTON_LIST,
                callback_data=QUERY_LIST
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
        return query.data == QUERY_LIST

    @classmethod
    def query_back(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_BACK

    @classmethod
    def query_add(cls, query: CallbackQuery) -> bool:
        return query.data == QUERY_ADD
