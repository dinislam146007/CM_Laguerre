# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from fake_useragent import UserAgent
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from get_coin_list import get_usdt_pairs
# from webdriver_manager.chrome import ChromeDriverManager
#
# useragent = UserAgent()
# # Конфигурация аккаунта TradingView
# TRADINGVIEW_EMAIL = "dinislam146007@gmail.com"
# TRADINGVIEW_PASSWORD = "899845_Dini"
#
#
# # Инициализация драйвера
# options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={useragent.random}")
# options.add_argument("--disable-blink-features=AutomationControlled")
# # options.add_argument('--proxy-server=138.128.91.65:8000')
# driver = webdriver.Chrome(options=options)
#
#
# def login():
#     try:
#         driver.get("https://www.tradingview.com/#signin")
#
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
#         WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys(
#             "dinislam146007@gmail.com")
#         driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
#         driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
#         time.sleep(25)
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
#         time.sleep(5)
#     except Exception as e:
#         print("Ошибка при входе в систему:", e)
#
#
#
# def process_symbol(symbol, interval):
#     driver.get(f'https://www.tradingview.com/chart/SHoYFzlp/?symbol=BYBIT%3A{symbol}&interval={interval}')
#     try:
#         invalid_text = WebDriverWait(driver, 5).until(
#             EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div')))
#         print('Scip')
#         return
#     except Exception:
#         pass
#     value_list = []
#     for i in range(1, 9):
#         value = WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located((By.XPATH,
#                                               f'/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div[{i}]/div'))
#         )
#         value_list.append(value.text)
#     pctRankT = float(value_list[0].replace('−', '-'))
#     pctile = float(value_list[1].replace('−', '-'))
#     pctRankB = float(value_list[3].replace('−', '-'))
#     pctileB = float(value_list[4].replace('−', '-'))
#     if pctRankT >= pctile:
#         print(f"Флаг Красный!\n Инструмент: {symbol}")
#     if pctRankB <= pctileB:
#         print(f'Фдаг Саламтовый\nИнструмент: {symbol}')
#
#
#
# # Функции для запуска задач с интервалами
# def run_tasks(interval, sleep_time):
#     while True:
#         for symbol in all_coins:
#             print(f"Начинаем обработку {symbol} на интервале {interval}")
#             process_symbol(symbol, interval)
#             print(f"Завершена обработка {symbol} на интервале {interval}")
#         print(f"Завершены все задачи для интервала {interval}. Ждем {sleep_time} секунд.")
#         time.sleep(sleep_time)
#
#
# all_coins = get_usdt_pairs()[21:]
#
#
# if __name__ == "__main__":
#     try:
#         login()
#         run_tasks('1H', 3600)
#     finally:
#         driver.quit()


def function():
    with open('INPUT.TXT', 'r') as f:
        print(f)


print(function())
