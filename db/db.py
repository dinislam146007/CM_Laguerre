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

    if row is None or (row != (pctRankT, pctile, pctRankB, pctileB)):
        # Обновляем или вставляем данные
        cursor.execute("""
        INSERT OR REPLACE INTO signals (symbol, interval, pctRankT, pctile, pctRankB, pctileB, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, interval, pctRankT, pctile, pctRankB, pctileB, datetime.now()))
        conn.commit()
        return True  # Значения обновились
    return False  # Значения не изменились
