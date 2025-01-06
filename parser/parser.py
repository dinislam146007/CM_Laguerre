import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from db.db import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image
import io
import base64
from collections import Counter

import datetime
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from matplotlib import colors
from collections import deque
from collections import deque
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.colors as colors
import pickle
from parser.get_coin_list import get_usdt_pairs

# Функции для работы с cookies


# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
driver.maximize_window()



TRADINGVIEW_EMAIL = "dinislam146007@gmail.com"
TRADINGVIEW_PASSWORD = "899845_Dini"
TR_LINK = 'SHoYFzlp'

def save_cookies(path='cookies.pkl'):
    """Сохранение cookies в файл."""
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(path='cookies.pkl'):
    """Загрузка cookies из файла."""
    try:
        # Загрузка cookies
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            # Перейдите на нужную страницу перед добавлением cookies
            driver.get("https://www.tradingview.com")
            for cookie in cookies:
                driver.add_cookie(cookie)
        return True
    except FileNotFoundError:
        print("Файл cookies не найден. Требуется ручной вход.")
        return False

def login(email):
    try:
        driver.get("https://www.tradingview.com/#signin")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys(email)
        driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
        # driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
        time.sleep(35)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
        time.sleep(10)
        save_cookies()
    except Exception as e:
        print("Ошибка при входе в систему:", e)

def process_colors(colors):
    finish = 'ignore'
    for color in colors:
        if color == 'Продажа':
            finish = 'sale'
        elif color == 'Покупка':
            finish = 'buy'
    return finish

def process_symbol(symbol, interval, link, signal_queue):
    try:
        # Открываем URL
        url = f'https://www.tradingview.com/chart/{link}/?symbol=BYBIT%3A{symbol}&interval={interval}'
        driver.get(url)
        print('get url')
        # time.sleep(10)
        # second_canvas  = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]')
        xpath = '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]'
        second_canvas = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        colors = []

        # Инициализируем ActionChains для управления мышью
        action = ActionChains(driver)

        # Определяем размеры canvas
        canvas_width = second_canvas.size['width']
        num_points = 150  # Количество точек для наведения
        
        # Начинаем с левого края графика и двигаемся вправо
        step = max(1, canvas_width // num_points)  # Шаг перемещения мыши
        for x in range(0, canvas_width, step):
            try:
                # Перемещаем курсор на позиции (x, canvas_height // 2)
                action.move_to_element_with_offset(second_canvas, x, 10).click_and_hold().perform()
                action.release().perform()

                # Сбор данных с текущей позиции
                value_list = []
                for i in range(1, 6):  # Цикл для чтения значений по XPATH
                    xpath = f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[{i}]/div'
                    value = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    value_list.append(value.text)

                # Обработка полученных данных
                if value_list:
                    try:
                        pctRankT = float(value_list[0].replace('−', '-'))
                        pctile = float(value_list[1].replace('−', '-'))
                        pctRankB = float(value_list[3].replace('−', '-'))
                        pctileB = float(value_list[4].replace('−', '-'))

                        # Анализ данных
                        if pctRankT >= pctile:
                            colors.append('Продажа')
                            # print('Продажа')
                        elif pctRankB <= pctileB:
                            colors.append('Покупка')
                            # print('Покупка')
                        else:
                            colors.append('Игнор')
                            # print('Игнор')
                    except ValueError:
                        print("Ошибка преобразования данных.")
                        continue
            except Exception as e:
                pass

                # print(f"Ошибка получения данных: {e}")
        buy_xpath = '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[3]/span[2]/span[1]'
        buy_price = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, buy_xpath)))
        buy_price = float(buy_price.text.replace(',', ''))
        sale_path = '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[1]/span[2]/span[1]'
        sale_price = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, sale_path)))
        sale_price = float(sale_price.text.replace(',', ''))
        print(buy_price, sale_price)

        finish = process_colors(colors)
        user_ids = get_all_user_id()
        now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')

        if finish == 'buy':
            # old = get_signal(symbol, interval)
            # if old:
            #     if old['status'] == 'buy':
            #         pass
            #     elif old['status'] == 'sale':
            for user_id in user_ids:
                pairs = str(user_id['crypto_pairs']).split(',')
                if (symbol in pairs) and (get_order(interval, symbol, user_id['user_id']) is None):
                    price = (user_id['percent'] / 100) * user_id['balance']
                    minus_plus_user(-price, user_id['user_id'])
                    buy_order(user_id['user_id'], interval, symbol, price, now, buy_price)
            # else:
            #     for user_id in user_ids:
            #         price = (user_id['percent'] / 100) * user_id['balance']
            #         minus_plus_user(-price, user_id['user_id'])
            #         buy_order(user_id['user_id'], interval, symbol, price, now, buy_price)
                
        elif finish == 'sale':
            # old = get_signal(symbol, interval)
            # if old:
            #     if old['status'] == 'buy':
            for user_id in user_ids:
                if get_order(interval, symbol, user_id['user_id']):
                    order = get_order(interval, symbol, user_id['user_id'])
                    coin_buy_price = order['coin_buy_price']  # старая цена
                    buy_price = order['buy_price']  # сумма закупки монеты
                    percent_change = ((sale_price - coin_buy_price) / coin_buy_price) * 100
                    profit_or_loss = (percent_change / 100) * buy_price
                    sale_order(user_id['user_id'], profit_or_loss, now)
        update_signal(symbol, interval, finish, buy_price, sale_price)  


    except Exception as e:
        print(f'Произошла ошибка №1 {e}')

def run_task(interval_list, signal_queue):
    """
    Основной цикл парсинга.
    """
    print('Начало коок')
    if not load_cookies():
        login(TRADINGVIEW_EMAIL)
    print('Конец куки')
    while True:
        for symbol in get_usdt_pairs():  # Замените на ваш список символов
            for interval in interval_list:
                process_symbol(symbol, interval, TR_LINK, signal_queue)
        time.sleep(5)
