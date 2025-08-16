import json
from datetime import datetime
import pathlib
import subprocess

from selenium.common.exceptions import NoSuchDriverException

import parse_with_selenium
import save_to_excel
import geocoding


def get_city_from_user():
    city = ""
    cities = []

    while True:
        print("Введите город, для которого требуется собрать прогноз погоды:")
        city = input("--> ")
        cities = geocoding.get_cities_coordinates(city)
        if len(cities) != 0:
            break
        print("Ничего не найдено! Попробуйте снова.")
    
    while True:
        print("Найдены следующие города:")
        for i in range(len(cities)):
            print(f"{i}. {cities[i].name} -- {cities[i].display_name}")
        print("Введите цифру нужного города:")
        selected_item = input("--> ")
        try:
            selected_item = int(selected_item)
            if selected_item >= 0 and selected_item < len(cities):
                return cities[selected_item]
        except:
            print("Ошибка при выборе! Попробуйте снова.")
        

if __name__ == "__main__":
    print("""
          ====================================================================================
            Запущена программа для получения прогноза погоды через сервис Яндекс Погода.
            Для работы программы на компьютере должен быть установлен браузер Google Chrome.
          ====================================================================================
          """)
    try:
        city = get_city_from_user()
    except KeyboardInterrupt:
        print("\nВвод прерван пользователь. Выход из программы...")
        quit()
    
    print(f"Выбранный город: {city.display_name}")

    print("Получение прогноза погоды. Пожалуйста, подождите...")
    try:
        url = f"https://yandex.ru/pogoda/ru?lat={city.lat}&lon={city.lon}"
        forecast = parse_with_selenium.parse(url)
    except NoSuchDriverException:
        print("\nНе найден подходящий браузер (Google Chrome) для запуска. Выход из программы...")
        quit()

    userpath = pathlib.Path.home().as_posix()

    current_datetime = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Forecast_{current_datetime}.xlsx"
    filepath = f"{userpath}/{filename}"

    save_to_excel.write_to_excel(city.display_name, forecast, filepath)
    
    print(f"Файл {filename} с прогнозом погоды создан в директории {userpath}")
    print("Открываю файл...")

    subprocess.Popen(["start", pathlib.Path(filepath)], shell=True)

    print("Завершение программы...")
