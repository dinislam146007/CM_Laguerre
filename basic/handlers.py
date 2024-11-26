from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
# from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InputFile, FSInputFile

router = Router()

@router.message(Command("start"))
async def start_message(message: Message):
    await message.answer(
        'Бот по обработке фильтра CM_Laguerre PPO PercentileRank Mkt Tops & Bottoms'
    )

