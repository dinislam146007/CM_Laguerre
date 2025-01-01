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



# Настройка Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

TRADINGVIEW_EMAIL = "dinislam146007@gmail.com"
TRADINGVIEW_PASSWORD = "899845_Dini"
TR_LINK = 'SHoYFzlp'


def login(email):
    try:
        driver.get("https://www.tradingview.com/#signin")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys(email)
        driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
        # driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
        time.sleep(10)
    except Exception as e:
        print("Ошибка при входе в систему:", e)

def process_symbol(symbol, interval, link):
    try:
        # Открываем URL
        url = f'https://www.tradingview.com/chart/{link}/?symbol=BYBIT%3A{symbol}&interval={interval}'
        driver.get(url)
        time.sleep(10)

        # Находим элемент графика по указанному пути
        graph_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[5]'))
        )

        # Получаем размеры видимой области графика
        bounding_rect = driver.execute_script("""
            const elem = arguments[0];
            const rect = elem.getBoundingClientRect();
            return {left: rect.left, top: rect.top, width: rect.width, height: rect.height};
        """, graph_element)

        # Параметры видимой области
        visible_width = int(bounding_rect['width'])
        visible_height = int(bounding_rect['height'])
        left_offset = int(bounding_rect['left'])
        print(f"Visible width: {visible_width}, height: {visible_height}, left: {left_offset}")

        colors = []
        action = ActionChains(driver)

        # Определяем количество точек для перемещения
        num_points = 94
        step = max(1, visible_width // num_points)  # Шаг по горизонтали

        # Середина по вертикали в видимой области
        y_position = visible_height // 2

        # Перемещаем курсор только по видимой области
        for x in range(0, visible_width, step):
            try:
                # Перемещаемся внутри видимой области графика
                action.move_to_element_with_offset(graph_element, x, y_position).perform()
                time.sleep(0.2)  # Ждем появления данных

                # Сбор данных (пример, как это делается)
                value_list = []
                for i in range(1, 6):  # Читаем данные по XPATH
                    xpath = f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[{i}]/div'
                    value = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    value_list.append(value.text)

                # Анализ данных
                if value_list:
                    try:
                        pctRankT = float(value_list[0].replace('−', '-'))
                        pctile = float(value_list[1].replace('−', '-'))
                        pctRankB = float(value_list[3].replace('−', '-'))
                        pctileB = float(value_list[4].replace('−', '-'))

                        # Логика анализа
                        if pctRankT >= pctile:
                            colors.append('Продажа')
                        elif pctRankB <= pctileB:
                            colors.append('Покупка')
                        else:
                            colors.append('Игнор')
                    except ValueError:
                        print("Ошибка преобразования данных.")
                        continue
            except Exception as e:
                print(f"Ошибка получения данных: {e}")
        print(colors)
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def run_task(interval_list, signal_queue):
    """
    Основной цикл парсинга.
    """
    login(TRADINGVIEW_EMAIL)
    while True:
        for symbol in ["BTCUSDT", "ETHUSDT"]:  # Замените на ваш список символов
            for interval in interval_list:
                process_symbol(symbol, interval, TR_LINK)
        time.sleep(5)
