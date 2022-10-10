import typing
from bot.keyboards.servers import ListItem


class AsListItemMixin:
    @classmethod
    async def as_list_items(cls, *args, **kwargs) -> ListItem:
        return list(map(lambda instance: (instance.__str__(), instance.id), await cls.filter(*args, **kwargs)))


class AsListAsyncItemMixin:
    async def __async_str__(self) -> str:
        raise NotImplemented('You need to implement `__async_str__` first.')

    @classmethod
    async def as_list_async_items(cls, *args, **kwargs) -> ListItem:
        async def wrapper(instance: cls) -> typing.Tuple[str, int]:
            return await instance.__async_str__(), instance.id

        list_of_items = []
        for model_object in await cls.filter(*args, **kwargs):
            list_of_items.append(await wrapper(model_object))

        return list_of_items
