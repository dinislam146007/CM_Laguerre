import sqlite3
from datetime import datetime

# Подключение к SQLite
conn = sqlite3.connect("trading_data.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    symbol TEXT,
    interval TEXT,
    pctRankT REAL,
    pctile REAL,
    pctRankB REAL,
    pctileB REAL,
    last_updated DATETIME,
    PRIMARY KEY (symbol, interval)
)
""")
conn.commit()

def update_signal(symbol, interval, pctRankT, pctile, pctRankB, pctileB):
    cursor.execute("""
    SELECT pctRankT, pctile, pctRankB, pctileB FROM signals WHERE symbol=? AND interval=?
    """, (symbol, interval))
    row = cursor.fetchone()
    print(f"Проверяем базу данных для {symbol} с интервалом {interval}: {row}")  # Отладочный вывод

    if row is None or (row != (pctRankT, pctile, pctRankB, pctileB)):
        print("Данные будут обновлены или вставлены.")  # Отладочный вывод
        cursor.execute("""
        INSERT OR REPLACE INTO signals (symbol, interval, pctRankT, pctile, pctRankB, pctileB, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, interval, pctRankT, pctile, pctRankB, pctileB, datetime.now()))
        conn.commit()
        return True  # Значения обновились
    print("Данные идентичны. Никаких изменений не происходит.")  # Отладочный вывод
    return False  # Значения не изменились
# update_signal('c', '1', 12.2, 12.2, 12,2, )


def get_signal():
    cursor.execute("""
    SELECT * FROM signals
    """)
    row = cursor.fetchall()
    return row

print(get_signal())
