import logging
from aiogram.dispatcher.filters.builtin import AdminFilter
from aiogram.types import CallbackQuery, Message
from keyboards.inline.game import admin_categories_keyboard
from misc import dp, g


async def edit_category(call: CallbackQuery, category):
    chat_id = call.message.chat.id
    if await AdminFilter().check(call):
        categories = g.get_chat_categories(chat_id)
        if category in categories:
            if len(categories) <= 1:
                await call.answer(text='Хотя бы одна категория должна быть выбрана')
                return
            action = 'remove'
            await call.answer(text='Категория удалена')
        else:
            action = 'add'
            await call.answer(text='Категория добавлена')
        g.edit_chat_category(chat_id=chat_id, category=category, action=action)
        return
    await call.answer(text='Только администаторы могут менять категории', show_alert=true)

@dp.message_handler(AdminFilter(), commands=['categories'])
async def set_categories(message: Message):
    await message.answer(
            text='Выберите категории, после чего используйте /play для запуска игры',
            reply_markup=admin_categories_keyboard,
            disable_notification=True
    )

@dp.message_handler(
        lambda message: g.in_play(chat_id=message.chat.id),
        AdminFilter(),
        commands=['stop']
)
async def stop_game(message: Message):
    g.change_state(chat_id=message.chat.id, state=0)
    await message.answer(
            text='Игра остановлена администратором',
            disable_notification=True
    )

@dp.callback_query_handler(text='movies')
async def movies_category(call: CallbackQuery):
    await edit_category(call=call, category='movies')

@dp.callback_query_handler(text='celebrities')
async def movies_category(call: CallbackQuery):
    await edit_category(call=call, category='celebrities')

@dp.callback_query_handler(text='general')
async def general_category(call: CallbackQuery):
    await edit_category(call=call, category='general')
