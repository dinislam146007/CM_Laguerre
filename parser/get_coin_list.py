import requests

def get_usdt_pairs():
    # URL для получения списка торговых инструментов
    url = "https://api.bybit.com/v5/market/instruments-info"

    # Параметры запроса
    params = {
        "category": "spot"  # Или "linear" для деривативов
    }

    try:
        # Отправляем запрос к API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем, что запрос выполнен успешно

        # Разбираем JSON-ответ
        data = response.json()

        if data['retCode'] == 0:  # Проверка успешного выполнения
            usdt_pairs = []
            for instrument in data['result']['list']:
                base_coin = instrument['baseCoin']
                if instrument['quoteCoin'] == "USDT" and not is_stablecoin(base_coin):
                    # Формируем пару базовая монета + USDT
                    pair = f"{base_coin}USDT"
                    usdt_pairs.append(pair)
            return usdt_pairs
        else:
            print("Ошибка API:", data['retMsg'])
            return []
    except requests.RequestException as e:
        print("Ошибка сети или API:", e)
        return []

def is_stablecoin(base_coin):
    """
    Определяет, является ли монета стейблкоином.
    """
    # Если в названии монеты есть признаки стейблкоина
    stablecoin_keywords = {"USD", "USDT", "USDC", "DAI", "BUSD", "TUSD", "PAX", "GUSD", "UST", "HUSD"}
    for keyword in stablecoin_keywords:
        if keyword in base_coin:
            return True
    return False



# Использование функции
# usdt_pairs_without_stablecoins = get_usdt_pairs()
# print("Пары, торгующиеся к USDT без стейблкоинов:", len(usdt_pairs_without_stablecoins))
