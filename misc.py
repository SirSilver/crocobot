import logging
import os
from aiogram import Bot, Dispatcher
from game import Game


bot = Bot(token=os.getenv('CROCOBOT_TOKEN'))
dp = Dispatcher(bot)
g = Game('crocobot.db')
logging.basicConfig(level=logging.INFO)
