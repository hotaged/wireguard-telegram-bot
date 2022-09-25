from tortoise import models, fields


class TelegramUser(models.Model):
    telegram_id = fields.IntField(unique=True)
    is_admin = fields.BooleanField(default=False)

    wg_peers: fields.ReverseRelation['WireguardPeer']


class WireguardPeer(models.Model):
    peer_name = fields.CharField(max_length=32)

    tg_user: fields.ForeignKeyRelation['TelegramUser'] = fields.ForeignKeyField(
        'models.TelegramUser', related_name='wg_peers'
    )
    wg_server: fields.ForeignKeyRelation['WireguardPeer'] = fields.ForeignKeyField(
        'models.WireguardServer', related_name='wg_peers'
    )


class WireguardServer(models.Model):
    webhook_url = fields.CharField(max_length=128)
    server_key = fields.CharField(max_length=256)
    country = fields.CharField(max_length=256)

    wg_peers: fields.ReverseRelation[WireguardPeer]


