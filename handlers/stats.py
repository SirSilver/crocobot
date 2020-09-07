from aiogram.types import Message
from misc import dp, g


@dp.message_handler(commands=['score'])
async def get_score(message: Message):
    player_id = message.from_user.id
    score = g.get_score(chat_id=message.chat.id, player_id=player_id)
    await message.answer(
            text=f'{g.get_player_name(player_id)}'
            f'\nОчков в этом чате: {score}'
    )

@dp.message_handler(commands=['scoretable'])
async def get_score_table(message: Message):
    table = g.get_score_table(chat_id=message.chat.id)
    text = 'Таблица топ10 игроков этого чата:'
    for score in table:
        text += f'\n{score[0]} - {score[1]}'
    await message.answer(text)
