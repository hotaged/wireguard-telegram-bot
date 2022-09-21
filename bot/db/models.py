from tortoise import models, fields


class TelegramUser(models.Model):
    telegram_id = fields.IntField()
    is_admin = fields.BooleanField(default=False)
