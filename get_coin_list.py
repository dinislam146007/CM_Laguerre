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
                if instrument['quoteCoin'] == "USDT":  # Фильтруем пары с базовой валютой USDT
                    # Формируем пару базовая монета + USDT
                    pair = f"{instrument['baseCoin']}USDT"
                    usdt_pairs.append(pair)
            return usdt_pairs
        else:
            print("Ошибка API:", data['retMsg'])
            return []
    except requests.RequestException as e:
        print("Ошибка сети или API:", e)
        return []

# Использование функции
# usdt_pairs = get_usdt_pairs()
# print("Пары, торгующиеся к USDT:", usdt_pairs)
