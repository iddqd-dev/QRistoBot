from aiogram import Bot, Dispatcher
from core.logger import create_logger


TOKEN = ''
logger = create_logger()
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)