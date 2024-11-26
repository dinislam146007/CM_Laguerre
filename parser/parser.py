import time
import asyncio
import threading
from selenium import webdriver
from fake_useragent import UserAgent
from parser.get_coin_list import get_usdt_pairs
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from concurrent.futures import ThreadPoolExecutor

from db.db import *

useragent = UserAgent()

# Создаем экземпляр Selenium WebDriver с асинхронным использованием
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Конфигурация аккаунтов TradingView
TRADINGVIEW_EMAIL = "dinislam146007@gmail.com"
TR_LINK = 'SHoYFzlp'
TRADINGVIEW_PASSWORD = "899845_Dini"

all_coins = get_usdt_pairs()
print(len(all_coins))


# Асинхронная функция для логина
def login(email):
    try:
        driver.get("https://www.tradingview.com/#signin")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys(email)
        driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
        driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
        time.sleep(30)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
        time.sleep(5)
    except Exception as e:
        print("Ошибка при входе в систему:", e)


# Асинхронная обработка символов с использованием ThreadPoolExecutor
def process_symbol(symbol, interval, link):
    try:
        url = f'https://www.tradingview.com/chart/{link}/?symbol=BYBIT%3A{symbol}&interval={interval}'
        driver.get(url)
        value_list = []

        for i in range(1, 7):
            xpath = f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[{i}]/div'
            value = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            value_list.append(value.text)

        if value_list:
            pctRankT = float(value_list[0].replace('−', '-'))
            pctile = float(value_list[1].replace('−', '-'))
            pctRankB = float(value_list[3].replace('−', '-'))
            pctileB = float(value_list[4].replace('−', '-'))

            print(pctRankT, pctile, pctRankB, pctileB)

            # Обновление базы данных
            if not update_signal(symbol, interval, pctRankT, pctile, pctRankB, pctileB):
                if pctRankT >= pctile:
                    print(f"Флаг Красный!\n Инструмент: {symbol}")
                if pctRankB <= pctileB:
                    print(f'Флаг Саламтовый\nИнструмент: {symbol}')
    except Exception as e:
        print("Ошибка в процессе символа:", e)


def _process_symbol(symbol, interval, link):
    try:
        url = f'https://www.tradingview.com/chart/{link}/?symbol=BYBIT%3A{symbol}&interval={interval}'
        driver.get(url)
        value_list = []

        for i in range(1, 7):
            xpath = f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[{i}]/div'
            value = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            value_list.append(value.text)

        if value_list:
            pctRankT = float(value_list[0].replace('−', '-'))
            pctile = float(value_list[1].replace('−', '-'))
            pctRankB = float(value_list[3].replace('−', '-'))
            pctileB = float(value_list[4].replace('−', '-'))

            print(pctRankT, pctile, pctRankB, pctileB)

            # Обновление базы данных
            if not update_signal(symbol, interval, pctRankT, pctile, pctRankB, pctileB):
                if pctRankT >= pctile:
                    print(f"Флаг Красный!\n Инструмент: {symbol}")
                if pctRankB <= pctileB:
                    print(f'Флаг Саламтовый\nИнструмент: {symbol}')
    except Exception as e:
        print("Ошибка в процессе символа:", e)


# Основная функция для обработки всех символов
async def run_task(interval_list, email, link, bot):
    login(email)
    while True:
        for symbol in all_coins:
            for interval in interval_list:
                process_symbol(symbol, interval, link)
        # print(f"Обработка завершена для всех символов на интервалах {interval_list}")


# Основной запуск программы
async def main_parser():
    await run_task(['1D', '4H', '1H', '30'], TRADINGVIEW_EMAIL, TR_LINK)


# if __name__ == "__main__":
#     asyncio.run(main())
