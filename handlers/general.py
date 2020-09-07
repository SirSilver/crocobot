import logging
from aiogram.types import ChatType, Message
from misc import bot, dp, g


@dp.message_handler(ChatType.is_private)
async def add_to_group(message: Message):
    await message.answer(
            text='Для использования этого бота, добавьте его в группу',
            disable_notification=True
    )

@dp.message_handler(commands=['start'])
async def start_bot(message: Message):
    from handlers.setup import setup_game
    await setup_game(message=message)

@dp.message_handler(lambda message: message.is_command() and not g.chat_exists(message.chat.id))
async def not_started(message: Message):
    await message.answer(text='Начните исопльзование бота с команды /start')

@dp.message_handler(commands=['help'])
async def help_commands(message: Message):
    await message.answer(
            text='/play - Начать игру'
            '\n/score - Получить инофрмацию о своих очках'
            '\n/scoretable - Получить топ10 игроков в этом чате',
            disable_notification=True
    )
