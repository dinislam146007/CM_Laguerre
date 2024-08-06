import time
from selenium import webdriver

from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--proxy-server=138.128.91.65:8000')
driver = webdriver.Chrome(options=options)




url = 'https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT&interval=1H'
longInfo = ["dinislam146007", "899845_Dini"]
driver.get("https://www.tradingview.com/#signin")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='id_username']"))).send_keys("dinislam146007@gmail.com")
driver.find_element(By.XPATH, "//input[@name='id_password']").send_keys("899845_Dini")
driver.find_element(By.XPATH, "//span[@class='wrapper-GZajBGIm']").click()
time.sleep(15)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))).click()
time.sleep(5)

driver.get('https://www.tradingview.com/chart/SHoYFzlp/?symbol=BINANCE%3ABTCUSDT&interval=1H')
value = driver.find_element(By.CSS_SELECTOR, 'div.valueValue-l31H9iuA')
print(value.text)
time.sleep(15)

