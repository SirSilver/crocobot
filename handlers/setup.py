import logging
from aiogram.types import CallbackQuery, Message, ChatMember
from keyboards.inline.game import categories_keyboard, words_keyboard
from misc import dp, g


async def setup_game(message: Message):
    chat_id = message.chat.id
    if not g.chat_exists(chat_id):
        g.add_chat(chat_id, chat_name=message.chat.full_name)
        logging.info(f'Chat with id = {chat_id} added to database')
    if g.in_play(chat_id=chat_id):
        await message.answer(
                text=f'Игра уже в процессе!\n{g.get_speaker_name(chat_id)} - объясняющий',
                reply_markup=words_keyboard,
                disable_notification=True
        )
        return
    await set_categories(message=message)

@dp.message_handler(commands=['categories'])
async def set_categories(message: Message):
    await message.answer(
            text='Изменять категории могут администраторы.'
                '\nИспользуйте /play чтобы запустить игру с установленными категориям',
            reply_markup=categories_keyboard,
            disable_notification=True
    )

@dp.callback_query_handler(text='list')
async def get_categories(call: CallbackQuery):
    categories = g.get_chat_categories(chat_id=call.message.chat.id)
    text = ''
    if 'movies' in categories:
        text += 'Фильмы\n'
    if 'celebrities' in categories:
        text += 'Знаменитости\n'
    if 'general' in categories:
        text += 'Общее\n'
    await call.answer(text=text, show_alert=True)
