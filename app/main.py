from enum import Enum
from datetime import datetime
import pathlib
import subprocess
import traceback

from selenium.common.exceptions import NoSuchDriverException

import parse_with_selenium
import save_to_excel
import geocoding
import database


def get_city_from_user():
    city = ""
    cities = list()

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
        print("Введите цифру нужного города или '9' для выхода из программы.")
        selected_item = input("--> ")
        try:
            selected_item = int(selected_item)
            if selected_item == 9:
                return None
            if selected_item >= 0 and selected_item < len(cities):
                return cities[selected_item]
        except:
            print("Ошибка при выборе! Попробуйте снова.")

def resolve_program_path(program_name):
    home_path = pathlib.Path.home().as_posix()
    program_path = pathlib.Path(f"{home_path}/{program_name}")
    program_path.mkdir(exist_ok=True)
    return program_path.as_posix()


class ResultMessages(Enum):
    KEYBOARD_INTERRUPT = "[FAILED] User interrupted the input during choosing the city."
    EXITED_BY_USER = "[FAILED] User quit during choosing the city."
    BROWSER_NOT_FOUND = "[FAILED] Browser Google Chrome is not intstalled."
    FILE_NOT_SAVED = "[FAILED] Can't save the file."
    FILE_NOT_OPENED = "[FAILED] Can't open the file."
    SUCCESS = "[SUCCESS]"

# TODO: migrate logs to smth else? mb function? since there is a lot repeated code in the except statements
if __name__ == "__main__":
    print("""
          ====================================================================================
            Запущена программа для получения прогноза погоды через сервис Яндекс Погода.
            Для работы программы на компьютере должен быть установлен браузер Google Chrome.
          ====================================================================================
          """)
    try:
        homepath = resolve_program_path("forecast_parser")
        db = database.Database(homepath)
    # TODO: different exceptions for getting path and opening database
    except:
        print("\nОшибка при подключении к базе данных логов! Выполнение программы не может быть продолжено!"
              + "\nПожалуйста, предоставьте ошибку ниже разработчику:")
        
        print("[ERROR START]\n"
              + traceback.format_exc()
              + "[ERROR END]")

        print("\nВыход из программы...")
        quit()

    try:
        city = get_city_from_user()
        if city == None:
            print("Завершение программы...")
            db.save_log("", datetime.today(), ResultMessages.EXITED_BY_USER.value)
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем. Выход из программы...")
        db.save_log("", datetime.today(), ResultMessages.KEYBOARD_INTERRUPT.value, traceback.format_exc())
        quit()
    
    print(f"Выбранный город: {city.display_name}")

    print("Получение прогноза погоды. Пожалуйста, подождите...")
    try:
        url = f"https://yandex.ru/pogoda/ru?lat={city.lat}&lon={city.lon}"
        forecast = parse_with_selenium.parse(url)
    except NoSuchDriverException:
        print("\nНе найден подходящий браузер (Google Chrome) для запуска. Выход из программы...")
        db.save_log(city.display_name, datetime.today(), ResultMessages.BROWSER_NOT_FOUND.value, traceback.format_exc())
        quit()

    filename = f"Forecast_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    filepath = f"{homepath}/{filename}"

    try:
        save_to_excel.write_to_excel(city.display_name, forecast, filepath)
    except:
        print("\nОшибка при сохранении конечного файла. Выход из программы...")
        db.save_log(city.display_name, datetime.today(), ResultMessages.FILE_NOT_SAVED.value, traceback.format_exc())
        quit()
    
    print(f"\nФайл {filename} с прогнозом погоды создан в директории {homepath}")
    print("Открываю файл...")

    try:
        subprocess.Popen(["start", pathlib.Path(filepath)], shell=True)
    except:
        print("\nОшибка при открытии файла с прогнозом погоды. Попробуйте открыть самостоятельно.\
               \nВыход из программы...")
        db.save_log(city.display_name, datetime.today, ResultMessages.FILE_NOT_SAVED.value, traceback.format_exc())
        quit()

    db.save_log(city.display_name, datetime.today(), ResultMessages.SUCCESS.value, "")
    db.close_connection()

    input("\nНажмите ENTER для выхода.")
