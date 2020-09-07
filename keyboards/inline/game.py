from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


words_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Посмотреть слово', callback_data='show_word')
            ],
            [
                InlineKeyboardButton(text='Изменить слово', callback_data='change_word')
            ]
        ]
)

admin_categories_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Фильмы', callback_data='movies'),
                InlineKeyboardButton(text='Знаменитости', callback_data='celebrities'),
                InlineKeyboardButton(text='Общее', callback_data='general')
            ],
            [
                InlineKeyboardButton(text='Выбранные категории', callback_data='list')
            ]
        ]
)

categories_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Выбранные категории', callback_data='list')
            ]
        ]
)
