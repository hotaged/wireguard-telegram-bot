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


class WireguardServer(models.Model, AsListItemMixin):
    webhook_url = fields.CharField(max_length=128)
    server_key = fields.CharField(max_length=256)
    country = fields.CharField(max_length=256)

    wg_peers: fields.ReverseRelation[WireguardPeer]

    def __str__(self) -> str:
        return self.country

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
