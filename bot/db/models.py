import ujson
import typing
import aiohttp
from aiohttp import ClientConnectionError

from tortoise import models, fields
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


class TelegramUser(models.Model, AsListItemMixin):
    telegram_id = fields.IntField(unique=True)
    is_admin = fields.BooleanField(default=False)

    wg_peers: fields.ReverseRelation['WireguardPeer']

    def __str__(self) -> str:
        return f'User<id: {self.telegram_id}>'


class WireguardPeer(models.Model, AsListItemMixin):
    peer_name = fields.CharField(max_length=32)

    tg_user: fields.ForeignKeyRelation['TelegramUser'] = fields.ForeignKeyField(
        'models.TelegramUser', related_name='wg_peers', null=True
    )
    wg_server: fields.ForeignKeyRelation['WireguardPeer'] = fields.ForeignKeyField(
        'models.WireguardServer', related_name='wg_peers'
    )

    def __str__(self) -> str:
        return self.peer_name

    async def config_and_qrcode(self) -> typing.Tuple[str, bytes]:
        headers = {'x-api-token': self.wg_server.server_key}

        webhook_config_url = f'{self.wg_server.webhook_url}/{self.peer_name}/config'
        webhook_qrcode_url = f'{self.wg_server.webhook_url}/{self.peer_name}/qrcode'

        async with aiohttp.ClientSession(headers=headers) as client:
            async with client.get(webhook_config_url) as response:
                config = await response.text()

            async with client.get(webhook_qrcode_url) as response:
                qrcode = await response.read()

        return config, qrcode


class WireguardServer(models.Model, AsListItemMixin, AsListAsyncItemMixin):
    webhook_url = fields.CharField(max_length=128)
    server_key = fields.CharField(max_length=256)
    country = fields.CharField(max_length=256)

    wg_peers: fields.ReverseRelation[WireguardPeer]

    def __str__(self) -> str:
        return self.country

    async def __async_str__(self) -> str:
        peers_amount = await self.wg_peers.all().count()
        peers_taken = await self.wg_peers.all().exclude(tg_user=None).count()

        return f'{self.__str__()} ({peers_taken}/{peers_amount})'

    async def download_peers(self) -> bool:
        headers = {'x-api-token': self.server_key}

        try:
            async with aiohttp.ClientSession(headers=headers) as client:
                async with client.get(self.webhook_url) as response:
                    if response.status != 200:
                        await self.delete()
                        return False

                    peers: typing.List[str] = await response.json(loads=ujson.loads)

                    for peer_name in peers:
                        await WireguardPeer.create(
                            peer_name=peer_name,
                            wg_server=self
                        )
        except ClientConnectionError:
            await self.delete()
            return False

        return True

    async def available_peers(self):
        return self.wg_peers.filter(tg_user=None)

    @classmethod
    async def list_countries(cls) -> typing.List[str]:
        return list(await cls.all().values_list('country', flat=True))

    @classmethod
    async def get_by_country(cls, country: str) -> typing.Union['WireguardServer', None]:
        servers = await cls.filter(country=country)

        if not len(servers):
            return None

        async def available_peers_count(instance: WireguardServer) -> int:
            return await (await instance.available_peers()).count()

        current_server = servers[0]
        current_server_peers_count = available_peers_count(servers[0])

        if len(servers) > 1:
            for server in servers[1:]:
                if ((server_peers_count := await available_peers_count(server))
                        > await current_server_peers_count):
                    current_server_peers_count = server_peers_count
                    current_server = server

        return current_server

