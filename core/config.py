from aiogram import Bot, Dispatcher
from core.logger import create_logger


TOKEN = '6001789387:AAGbfcyEgEYIhEvzLjbPNeBN-Bb6g0pXiVk'
logger = create_logger()
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)