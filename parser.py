import time
import threading
from selenium import webdriver
from fake_useragent import UserAgent
from get_coin_list import get_usdt_pairs
import asyncio
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from db.db import *

useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# # options.add_argument(f"user-agent={useragent.random}")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--proxy-server=138.128.91.65:8000')
driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Конфигурация аккаунтов TradingView
TRADINGVIEW_EMAIL = "dinislam146007@gmail.com"
TR_LINK = 'SHoYFzlp'
TRADINGVIEW_PASSWORD = "899845_Dini"

all_coins = get_usdt_pairs()

print(len(all_coins))

def create_driver():
    pass
def login(email):
    try:
        driver.get("https://www.tradingview.com/#signin")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys(email)
        driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
        driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
        time.sleep(30)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
        time.sleep(5)
    except Exception as e:
        print("Ошибка при входе в систему:", e)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def process_symbol(symbol, interval, link):
    try:
        url = f'https://www.tradingview.com/chart/{link}/?symbol=BYBIT%3A{symbol}&interval={interval}'
        driver.get(url)
        value_list = []

        for i in range(1, 9):
            try:
                value = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div[{i}]/div'))
                )
                value_list.append(value.text)
            except (NoSuchElementException, TimeoutException):
                return

        if value_list:
            pctRankT = float(value_list[0].replace('−', '-'))
            pctile = float(value_list[1].replace('−', '-'))
            pctRankB = float(value_list[3].replace('−', '-'))
            pctileB = float(value_list[4].replace('−', '-'))

            # Обновление базы данных
            if update_signal(symbol, interval, pctRankT, pctile, pctRankB, pctileB):
                # Логика обработки только при изменении данных
                if pctRankT >= pctile:
                    print(f"Флаг Красный!\n Инструмент: {symbol}")
                if pctRankB <= pctileB:
                    print(f'Флаг Саламтовый\nИнструмент: {symbol}')
    except Exception as e:
        print("Ошибка в процессе символа:", e)

def run_task(interval_list, email, link):
    login( email)
    while True:
        for symbol in all_coins:
            for interval in interval_list:
                print(f"Начинаем обработку {symbol} на интервале {interval}")
                process_symbol(symbol, interval, link)
                print(f"Завершена обработка {symbol} на интервале {interval}")


def main():
    run_task(['1D', '4H', '1H', '30'], TRADINGVIEW_EMAIL, TR_LINK)


if __name__ == "__main__":
    main()
