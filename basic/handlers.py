from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InputFile, FSInputFile
from db.db import *
from parser.get_coin_list import get_usdt_pairs

router = Router()

class EditPercent(StatesGroup):
    new = State()

class CryptoPairs(StatesGroup):
    pairs = State()


def interval_conv(interval):
    if interval == '1D':
        return '1Д'
    elif interval == '4H':
        return '4h'
    elif interval == '1H':
        return '1h'
    elif interval == '30':
        return '30m'
    
def buy_sale(status, interval):
    if status == 'buy':
        return f'🔰{interval} - B;'
    else:
        return f"🔻{interval} - S;"

@router.callback_query(F.data.startswith('like'))
async def like_symbol(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split()[1]
    user = get_user(callback.from_user.id)
    if action == 'start':
        msg = 'Раздел избранные пары\n\n'
        if user['crypto_pairs']:
            msg += f"Ваш список избранных пар: {user['crypto_pairs']}"
        else:
            msg += 'Список избранных пар пока пуст'
        await callback.message.edit_text(
            text=msg,
            reply_markup=like_inline()
        )
    elif action == 'add':
        msg = 'Введите одну пару или несколько пар через запятую\n\nПример: BTCUSDT,EGLDUSDT,XDCUSDT'
        await state.set_state(CryptoPairs.pairs)
        msg = await callback.message.edit_text(
            text=msg,
            reply_markup=close_state()
        )
        await state.update_data(action=action, last_msg=msg.message_id)

    else:
        if user['crypto_pairs']:
            msg = 'Введите одну пару или несколько пар через запятую\n\nПример: BTCUSDT,EGLDUSDT,XDCUSDT'
            await state.set_state(CryptoPairs.pairs)
            msg = await callback.message.edit_text(
                text=msg,
                reply_markup=close_state()
            )
            await state.update_data(action=action, last_msg=msg.message_id)

        else:
            await callback.answer('У вас нет пар для удаления')



@router.message(CryptoPairs.pairs)
async def add_del_pairs(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    valid_pairs = get_usdt_pairs()

    # Получаем список пар из сообщения
    user_input = message.text
    pairs = [pair.strip().upper() for pair in user_input.split(',')]  # Разделяем, очищаем и приводим к верхнему регистру

    # Проверяем, что пользователь ввёл корректные пары
    invalid_pairs = [pair for pair in pairs if pair not in valid_pairs]
    if invalid_pairs:
        await message.answer(f"Некорректные пары: {', '.join(invalid_pairs)}.\n\nВведите корректные пары.")
        return

    if not pairs or any(not pair for pair in pairs):
        await message.answer("Некорректный ввод. Введите пары через запятую, например: BTCUSDT,ETHUSDT")
        return
    
    if data['action'] == 'add':
        for pair in pairs:
            await add_crypto_pair_to_db(message.from_user.id, pair)  # Функция добавления пары в базу
        await message.answer(f"Добавлены пары: {', '.join(pairs)}")
    else:
        for pair in pairs:
            await delete_crypto_pair_from_db(message.from_user.id, pair)  # Функция удаления пары из базы
        await message.answer(f"Удалены пары: {', '.join(pairs)}")
    msg = 'Раздел избранные пары\n\n'
    user = get_user(message.from_user.id)
    if user['crypto_pairs']:
        msg += f"Ваш список избранных пар: {user['crypto_pairs']}"
    else:
        msg += 'Список избранных пар пока пуст'
    await message.answer(
        text=msg,
        reply_markup=like_inline()
    )

    await state.clear()

@router.callback_query(F.data.startswith('stat'))
async def statistics(callback: CallbackQuery, ):
    action = callback.data.split()[1]
    if action == 'start':
        msg = 'Раздел статистика\n\n'
        msg += 'Ваши сделки'
        profit = len(get_stat_db(callback.from_user.id, 'profit'))
        lois = len(get_stat_db(callback.from_user.id, 'loise'))
        await callback.message.edit_text(
            text=msg,
            reply_markup=stat_inline(profit, lois)
        )



@router.message(Command("start"))
async def start_message(message: Message, bot: Bot):
    if not get_user(message.from_user.id):
        set_user(message.from_user.id, 5.0, 50000.0)
    user = get_user(message.from_user.id)
    await message.answer(
        f"Бот по обработке фильтра CM_Laguerre PPO PercentileRank Mkt Tops & Bottoms\nВаш баланс: {user['balance']}",
        reply_markup=start_inline()
    )

@router.callback_query(F.data.startswith('orders'))
async def orders(callback: CallbackQuery, bot: Bot):
    action = callback.data.split()[1]
    if action == 'start':
        open = len(get_all_orders(callback.from_user.id, 'open'))
        close = len(get_all_orders(callback.from_user.id, 'close'))
        await callback.message.edit_text(
            text='Ваши сделки', 
            reply_markup=orders_inline(open, close)
        )
    else:
        forms = get_all_orders(callback.from_user.id, action)
        n = int(callback.data.split()[2])
        form = forms[n]
        msg = f"Инструмент: {form['symbol']}\n"
        msg += f"ТФ: {form['interval']}\n"
        msg += f"Цена за монету: {form['coin_buy_price']}\n"
        msg += f"Куплено на {form['buy_price']}\n"
        msg += f"Дата и время покупки: {form['buy_time']}\n"
        if action == 'close':
            msg += f"Продано за {form['sale_price']}\n"
            msg += f"Дата и время продажи: {form['sale_time']}"
        await callback.message.edit_text(
            text=msg,
            reply_markup=orders_inline_n(n, action, len(forms))
        )

async def split_message_and_edit(bot_message, text, reply_markup=None):
    while len(text) > 4096:
        chunk = text[:4096].rsplit('\n', 1)[0]  # Разбить по строкам
        await bot_message.edit_text(text=chunk)
        text = text[len(chunk):]
    await bot_message.edit_text(text=text, reply_markup=reply_markup)

    
@router.callback_query(F.data.startswith('signals'))
async def signals(callback: CallbackQuery, bot: Bot):
    action = callback.data.split()[1]
    if action == 'start':
        sale = count_signals('sale')
        buy = count_signals('buy')
        # forms = all_signals_no_signal()
        # old_symbol = 'start'
        # msg_parts = []
        # for form in forms:
        #     if old_symbol != form['symbol']:
        #         if old_symbol == 'start':
        #             msg_parts.append(f"{form['symbol']} - {buy_sale(form['status'], interval_conv(form['interval']))}")
        #         else:
        #             msg_parts.append(f"\n{form['symbol']} - {buy_sale(form['status'], interval_conv(form['interval']))}")
        #         old_symbol = form['symbol']
        #     else:
        #         msg_parts.append(buy_sale(form['status'], interval_conv(form['interval'])))
        #         old_symbol = form['symbol']

        # msg = "".join(msg_parts)
        # await split_message_and_edit(callback.message, msg, signals_inline(buy, sale))
        await callback.message.edit_text(
            text='Сигналы', 
            reply_markup=signals_inline(buy, sale)
        )
    else:
        interval = action.split('_')[1]
        action = action.split('_')[0]
        if interval == 's':
            forms = all_signals_no_signal()
            old_symbol = 'start'
            msg_parts = []
            for form in forms:
                if old_symbol != form['symbol']:
                    if old_symbol == 'start':
                        msg_parts.append(f"{form['symbol']} - {buy_sale(form['status'], interval_conv(form['interval']))}")
                    else:
                        msg_parts.append(f"\n{form['symbol']} - {buy_sale(form['status'], interval_conv(form['interval']))}")
                    old_symbol = form['symbol']
                else:
                    msg_parts.append(buy_sale(form['status'], interval_conv(form['interval'])))
                    old_symbol = form['symbol']
            msg = "".join(msg_parts)
            await split_message_and_edit(callback.message, msg, interval_inline(action))

            # await callback.message.edit_text(
            #     text=msg,
            #     reply_markup=interval_inline(action)
            # )
        else:
            # n = int(callback.data.split()[2])
            forms = all_signals(action, interval)
            # form = forms[n]
            if action == 'sale':
                signal = 'продажу'
            else:
                signal = 'покупку'
            msg = f"Сигнал на {signal}\n"
            # msg += f"Инструмент: {form['symbol']}\n"
            msg += f"ТФ: {interval_conv(interval)}\n"
            for form in forms:
                msg += f"{form['symbol']} - {buy_sale(action, interval)}\n"
            # msg += f"Цена за покупку: {form['buy_price']}\n"
            # msg += f"Цена за продажу {form['sale_price']}"
            await split_message_and_edit(callback.message, msg, signals_inline_n(action))
    
            # await callback.message.edit_text(
            #     text=msg,
            #     reply_markup=signals_inline_n(action)
            # )


@router.callback_query(F.data.startswith('settings'))
async def settings(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split()[1]
    if action == 'start':
        user = get_user(callback.from_user.id)
        text = 'Параметры задействования ботом установленного процента от депозита для совершения сделок.\n\n'
        text += 'Чтобы изменить % от общего депозита на который будут совершаться сделки ботом, воспользуйтесь кнопкой "Изменить процент"\n\n'
        text += f"Текущий процент: {user['percent']}%"
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
