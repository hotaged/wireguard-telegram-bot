from tortoise import Tortoise, connections
from bot import settings


async def init():
    await Tortoise.init(
        db_url=settings.db_uri,
        modules={'models': ['bot.db.models']}
    )


async def shutdown():
    await connections.close_all()


TORTOISE_ORM = {
    'connections': {'default': settings.db_uri},
    'apps': {
        'models': {
            'models': ['bot.db.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}