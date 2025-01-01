from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InputFile, FSInputFile
from db.db import *

router = Router()

class EditPercent(StatesGroup):
    new = State()

@router.message(Command("start"))
async def start_message(message: Message):
    if not get_user(message.from_user.id):
        set_user(message.from_user.id, 5.0)
    await message.answer(
        'Бот по обработке фильтра CM_Laguerre PPO PercentileRank Mkt Tops & Bottoms',
        reply_markup=start_inline()
    )
    

@router.callback_query(F.data.startswith('settings'))
async def settings(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split()[1]
    if action == 'start':
        user = get_user(callback.from_user.id)
        text = f"Процент: {user[1]}\n"
        text += 'Изменить:'
        await callback.message.edit_text(
            text=text,
            reply_markup=settings_inline()
        )
    elif action == 'percent':
        msg = await callback.message.edit_text(
            'Введите новый процент',
            reply_markup=close_state()
        )
        await state.set_state(EditPercent.new)
        await state.update_data(last_msg=msg.message_id)
    

@router.message(EditPercent.new)
async def edit_percent(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    try:
        percent = float(message.text)
        up_percent(message.from_user.id, percent)
        await message.answer('Процент обновлен!')
        await state.clear()
    except ValueError:
        await message.answer(
            'Введите число!', 
            reply_markup=close_state()
        )
        return
    

@router.callback_query(F.data == 'close_state')
async def close_state_cal(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
    except Exception:
        pass
    await callback.message.edit_text(
        'Бот по обработке фильтра CM_Laguerre PPO PercentileRank Mkt Tops & Bottoms',
        reply_markup=start_inline()
    )

        


@router.callback_query(F.data == 'start')
async def start_cal(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Бот по обработке фильтра CM_Laguerre PPO PercentileRank Mkt Tops & Bottoms',
        reply_markup=start_inline()
    )
