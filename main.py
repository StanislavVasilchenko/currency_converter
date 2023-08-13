import json
import os
from datetime import datetime

import requests

API = os.getenv("EXCHANGE_RATE_API_KEY")
CURRENCY_RATES_FILE = "currency_rates.json"


def main():
    while True:
        currency = input("Введите название валюты (USD или EUR): ").upper()
        if currency not in ("USD", "EUR"):
            print("Некорректный ввод")
            continue
        rate = get_currency_rate(currency)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Курс {currency} к рублю: {rate}")

        data = {"currency": currency, "rate": rate, "timestamp": timestamp}

        save_to_json(data)

        choice = input("Выберите действие: (1 - продолжить, 2 - выйти) ")
        if choice == "1":
            continue
        elif choice == "2":
            break
        else:
            print("Некорректный ввод")


def get_currency_rate(base: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={"apikey": API}, params={"base": base})
    rate = response.json()["rates"]["RUB"]
    return rate


def save_to_json(date: dict) -> None:
    """Сохраняет данные в JSON-файл"""

    with open(CURRENCY_RATES_FILE, "a") as file:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([date], file)
        else:
            with open(CURRENCY_RATES_FILE) as file:
                data_list = json.load(file)
                data_list.append(date)
            with open(CURRENCY_RATES_FILE, "w") as file:
                json.dump(data_list, file)


if __name__ == '__main__':
    main()
