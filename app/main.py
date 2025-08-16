import json
from datetime import datetime
import pathlib
import subprocess

import parse_with_selenium
import save_to_excel

if __name__ == "__main__":
    # static for testing purposes
    # TODO: should be generated depending on input city later on
    url = "https://yandex.ru/pogoda/ru?lat=59.938784&lon=30.314997"

    forecast = parse_with_selenium.parse(url)
    print(json.dumps(forecast, indent=4, ensure_ascii=False))

    userpath = pathlib.Path.home().as_posix()

    current_datetime = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Forecast_{current_datetime}.xlsx"
    filepath = f"{userpath}/{filename}"

    save_to_excel.write_to_excel(forecast, filepath)
    
    print(f"Файл {filename} с прогнозом погоды создан в директории {userpath}")
    print("Открываю файл...")

    subprocess.Popen(["start", pathlib.Path(filepath)], shell=True)
