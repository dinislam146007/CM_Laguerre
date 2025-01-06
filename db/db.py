import sqlite3
from datetime import datetime

# Подключение к SQLite
conn = sqlite3.connect("trading_data.db")
cursor = conn.cursor()

# Создание таблицы
# Создание таблицы signals
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    symbol TEXT,
    interval TEXT,
    status TEXT,
    buy_price REAL,
    sale_price REAL,
    PRIMARY KEY (symbol, interval)  -- Уникальность по symbol и interval
)
""")

# Создание таблицы users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,  -- Уникальный идентификатор пользователя
    percent REAL,
    balance REAL,
    crypto_pairs TEXT
)
""")

# cursor.execute("""
# ALTER TABLE users ADD COLUMN crypto_pairs TEXT
# """)


# Создание таблицы orders
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    user_id INTEGER,
    symbol TEXT,
    interval TEXT,  -- Исправлена опечатка
    coin_buy_price REAL,
    buy_price REAL,
    sale_price REAL,
    buy_time TEXT,
    sale_time TEXT
)
""")

conn.commit()

def update_signal(symbol, interval, status, buy_price, sale_price):
    with sqlite3.connect("trading_data.db") as conn:  # Открываем новое соединение
        cursor = conn.cursor()  # Создаем новый курсор
        # Проверяем, есть ли запись с таким символом и интервалом
        cursor.execute("""
        SELECT status FROM signals WHERE symbol=? AND interval=?
        """, (symbol, interval))
        row = cursor.fetchone()

        print(f"Проверяем базу данных для {symbol} с интервалом {interval}: {row}")  # Отладочный вывод

        if row is None:
            # Если записи нет, вставляем новую
            print("Вставляем новую запись.")  # Отладочный вывод
            cursor.execute("""
            INSERT INTO signals (symbol, interval, status, buy_price, sale_price)
            VALUES (?, ?, ?, ?, ?)
            """, (symbol, interval, status, buy_price, sale_price))
        else:
            # Если запись есть, обновляем данные
            print("Обновляем существующую запись.")  # Отладочный вывод
            cursor.execute("""
            UPDATE signals
            SET status=?, buy_price=?, sale_price=?
            WHERE symbol=? AND interval=?
            """, (status, buy_price, sale_price, symbol, interval))

        conn.commit()  # Фиксируем изменения
        print("Данные успешно обновлены.")  # Отладочный вывод

def set_user(user_id, percent, balance):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, percent, balance)
        VALUES (?, ?, ?)
        """, (user_id, percent, balance))
        conn.commit()
        return True

def get_user(user_id):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM users WHERE user_id=?
        """, (user_id,))
        row = cursor.fetchone()
        if row is not None:
            # Создаем словарь с именами полей из запроса
            columns = [desc[0] for desc in cursor.description]  # Получаем названия колонок
            client_data = dict(zip(columns, row))  # Соединяем названия колонок и данные
            return client_data
        return None  # Если ничего не найдено, возвращаем None


def get_signals():
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM signals
        """)
        rows = cursor.fetchall()
        return rows
    
def get_stat_db(user_id, action):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        if action == 'profit':
            cursor.execute("""
            SELECT * FROM orders
            WHERE user_id=?
            AND sale_price>buy_price
            """, (user_id, ))
        else:
            cursor.execute("""
            SELECT * FROM orders
            WHERE user_id=?
            AND sale_price<buy_price
            """, (user_id, ))
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            # Создаем список словарей, где каждое поле строки сопоставлено названию колонки
            customer_data_list = [dict(zip(columns, row)) for row in rows]
            return customer_data_list  # Возвращаем список словарей
        return []  # Если ничего не найдено, возвращаем пустой список

    
def get_order(interval, symbol, user_id):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM orders
        WHERE symbol=? AND interval=? 
        AND sale_price IS NULL
        AND user_id =?
        """, (symbol, interval, user_id))
        row = cursor.fetchone()
        if row is not None:
            # Создаем словарь с именами полей из запроса
            columns = [desc[0] for desc in cursor.description]  # Получаем названия колонок
            client_data = dict(zip(columns, row))  # Соединяем названия колонок и данные
            return client_data
        return None  # Если ничего не найдено, возвращаем None

def buy_order(user_id, interval, symbol, buy_price, buy_time, coin_buy_price):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO orders (user_id, symbol, interval, buy_price, buy_time, coin_buy_price)
        VALUES (?, ?, ?, ?, ?, ?)""", (user_id, symbol, interval, buy_price, buy_time, coin_buy_price))
        conn.commit()    

def sale_order(user_id, sale_price, sale_time):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE orders SET sale_price=?, sale_time=?
        WHERE user_id=? AND sale_price IS NULL AND sale_time IS NULL
        """, (sale_price, sale_time, user_id, ))
        conn.commit()

def up_percent(user_id, percent):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users SET percent=?
        WHERE user_id=? 
        """, (percent, user_id, ))
        conn.commit()


async def add_crypto_pair_to_db(user_id: int, pair: str):
    # Здесь пишем логику для добавления пары в базу данных
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT crypto_pairs FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row and row[0]:  # Если есть данные
            existing_pairs = row[0].split(',')
            if pair not in existing_pairs:
                existing_pairs.append(pair)
        else:  # Если данных нет
            existing_pairs = [pair]

        pairs_str = ','.join(existing_pairs)
        cursor.execute("UPDATE users SET crypto_pairs = ? WHERE user_id = ?", (pairs_str, user_id))
        conn.commit()

async def delete_crypto_pair_from_db(user_id: int, pair: str):
    # Здесь пишем логику для удаления пары из базы данных
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT crypto_pairs FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row and row[0]:
            existing_pairs = row[0].split(',')
            if pair in existing_pairs:
                existing_pairs.remove(pair)

            pairs_str = ','.join(existing_pairs)
            cursor.execute("UPDATE users SET crypto_pairs = ? WHERE user_id = ?", (pairs_str, user_id))
            conn.commit()

        
def minus_plus_user(price, user_id):
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users
        SET balance = balance + ? 
        WHERE user_id=?
        """, (price, user_id, ))
        conn.commit()



def get_all_user_id():
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM users
        """)
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            # Создаем список словарей, где каждое поле строки сопоставлено названию колонки
            customer_data_list = [dict(zip(columns, row)) for row in rows]
            return customer_data_list  # Возвращаем список словарей
        return []  # Если ничего не найдено, возвращаем пустой список

    
def get_signal(symbol, interval):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM signals
        WHERE symbol=? AND interval=?
        """, (symbol, interval))
        row = cursor.fetchone()
        if row is not None:
            # Создаем словарь с именами полей из запроса
            columns = [desc[0] for desc in cursor.description]  # Получаем названия колонок
            client_data = dict(zip(columns, row))  # Соединяем названия колонок и данные
            return client_data
        return None  # Если ничего не найдено, возвращаем None


def count_signals(signal):
    with sqlite3.connect("trading_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COUNT(*) FROM signals
        WHERE status=?
        """, (signal,))
        row = cursor.fetchone()
        return row[0] if row else 0
    
def all_signals(status, interval):
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM signals
        WHERE status=? AND interval=?
        """, (status, interval))  # Добавлена запятая для формирования кортежа
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            # Создаем список словарей, где каждое поле строки сопоставлено названию колонки
            customer_data_list = [dict(zip(columns, row)) for row in rows]
            return customer_data_list  # Возвращаем список словарей
        return []  # Если ничего не найдено, возвращаем пустой список

def all_signals_no_signal():
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM signals
        """)  # Добавлена запятая для формирования кортежа
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            # Создаем список словарей, где каждое поле строки сопоставлено названию колонки
            customer_data_list = [dict(zip(columns, row)) for row in rows]
            return customer_data_list  # Возвращаем список словарей
        return []  # Если ничего не найдено, возвращаем пустой список


def get_all_orders(user_id, order_type):
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        if order_type == 'open':
            cursor.execute("""
            SELECT * FROM orders
            WHERE user_id=? 
            AND sale_price IS NULL
            """, (user_id, ))  # Добавлена запятая для формирования кортежа
        else:
            cursor.execute("""
            SELECT * FROM orders
            WHERE user_id=? 
            AND sale_price IS NOT NULL
            """, (user_id, ))  # Добавлена запятая для формирования кортежа

        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            # Создаем список словарей, где каждое поле строки сопоставлено названию колонки
            customer_data_list = [dict(zip(columns, row)) for row in rows]
            return customer_data_list  # Возвращаем список словарей
        return []  # Если ничего не найдено, возвращаем пустой список

