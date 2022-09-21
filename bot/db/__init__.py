from tortoise import Tortoise, connections
from bot import settings


async def init():
    await Tortoise.init(
        db_url=settings.db_uri,
        modules={'models': models}
    )


async def shutdown():
    await connections.close_all()


models = ['bot.db.models']


TORTOISE_ORM = {
    'connections': {'default': settings.db_uri},
    'apps': {
        'models': {
            'models': [*models, 'aerich.models'],
            'default_connection': 'default',
        },
    },
}