from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import settings

memory = MemoryStorage()

bot = Bot(settings.token)
dp = Dispatcher(bot, storage=memory)

