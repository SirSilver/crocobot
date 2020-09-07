import handlers
import logging
from aiogram import executor
from misc import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
