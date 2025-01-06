from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_inline():
    kb = [
        [InlineKeyboardButton(text='Сигналы 📌', callback_data='signals start'),
        InlineKeyboardButton(text='Статистика 📈', callback_data='stat start')],
        [InlineKeyboardButton(text='Сделки 📄', callback_data='orders start')],
        [InlineKeyboardButton(text='Избранные пары ⭐️', callback_data='like start')],
        [InlineKeyboardButton(text='Настройки ⚙️', callback_data='settings start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def stat_inline(profit, lesion):
    kb = [
        [
            InlineKeyboardButton(text=f'Прибыльные ({profit})', callback_data='stat profit'),
            InlineKeyboardButton(text=f'Убыточные ({lesion})', callback_data='stat lesion')
        ],
        [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def like_inline():
    kb = [
        [
            InlineKeyboardButton(text='Добавить пару', callback_data='like add'),
            InlineKeyboardButton(text='Удалить пару', callback_data='like del')
         ],
         [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def orders_inline(open, close):
    kb = [
        [
            InlineKeyboardButton(text=f'Открытые ({open})', callback_data='orders open 0'),
         InlineKeyboardButton(text=f'Закрытые ({close})', callback_data='orders close 0')
         ],
         [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def settings_inline():
    kb = [
        [InlineKeyboardButton(text='Изменить процент', callback_data='settings percent')],
        [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def close_state():
    kb = [
        [InlineKeyboardButton(text='Отмена', callback_data='close_state')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def signals_inline(buy, sale):
    kb = [
        [InlineKeyboardButton(text=f'🔰 Покупка ({buy})', callback_data='signals buy_s 0'), 
            InlineKeyboardButton(text=f'🔻 Продажа ({sale})', callback_data='signals sale_s 0')
            ],
            [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def signals_inline_n(status):
    kb = [
        # [InlineKeyboardButton(text=f"{n + 1} / {len_n}")]
        # [InlineKeyboardButton(text='<-', callback_data=f'signals {status}_{interval} {n - 1}'),
         [InlineKeyboardButton(text='Назад', callback_data=f'signals {status}_s')]
        #  InlineKeyboardButton(text='->', callback_data=f'signals {status}_{interval} {n + 1}')
        #  ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def orders_inline_n(n,status, len_n):
    kb = [
        [InlineKeyboardButton(text=f"{n+1}/{len_n}", callback_data="ignore")],
        [InlineKeyboardButton(text='<-', callback_data=f'orders {status} {n - 1}'),
         InlineKeyboardButton(text='Назад', callback_data='orders start'),
         InlineKeyboardButton(text='->', callback_data=f'orders {status} {n + 1}')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def interval_inline(status):
    kb = [
        [
            InlineKeyboardButton(text='ТФ - 1Д', callback_data=f'signals {status}_1D 0'),
        InlineKeyboardButton(text='ТФ - 4h', callback_data=f'signals {status}_4H 0'),
        InlineKeyboardButton(text='ТФ - 1h', callback_data=f'signals {status}_1H 0'),
        InlineKeyboardButton(text='ТФ - 30m', callback_data=f'signals {status}_30 0')
        ],
        [InlineKeyboardButton(text='Назад', callback_data=f'signals start 0')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)