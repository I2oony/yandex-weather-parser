# Парсинг данных сервиса Яндекс Погода в Excel-файл

Это консольное приложение на `Python`, используемое для получения прогноза погоды для выбранного города из сервиса Яндекс Погода.


## Системные требования

В настоящее время приложение поддерживает запуск и было протестировано на:

- `Windows 10`
- `Python 3.10.5`

А так же требует установленный `Google Chrome` для работы.

Работа приложения на других операционных системах семейства `Windows` не проверена. Работа на операционных системах семейства `Linux` не предусмотрена.


## Использование

### Запуск `.exe` файла
1. Скачать файл [dist/yandex_weather_parser.exe](/dist/yandex_weather_parser.exe).
2. Запустить скачанный файл.

### Запуск с установленным Python
1. Склонировать репозиторий.
2. Создать и запустить виртуальное окружение:
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```
3. Установить зависимости в окружение:
    ```cmd
    (venv) pip install -r app\requirements.txt
    ```
4. Запустить скрипт `main.py`:
   ```cmd
   python app\main.py
   ```
### Самостоятельная сборка `.exe` файла
1. Повторить шаги 1-3 пункта `Запуск с установленным Python`
2. Установить `pyinstaller`:
   ```cmd
   (venv) pip install pyinstaller
   ```
3. Собрать приложение из файла спецификации:
   ```cmd
   (venv) pyinstaller main.spec
   ```


## Политика использования

Настоящее приложение использует [Nominatim](https://nominatim.org/) - сервис геокодирования [OpenStreetMap](https://openstreetmap.org/). Приложение соотвествует [официальной политике использования Nominatim](https://operations.osmfoundation.org/policies/nominatim/). В случае создания форка на основе данного проекта с участием модуля [geocoding.py](/app/geocoding.py) **необходимо** указать своё приложение в переменную `NOMINATIM_USER_AGENT`.


## Авторы

[@I2oony](https://github.com/I2oony) - Полина Паламарь. E-mail для связи: [ppalamar28@gmail.com](mailto:ppalamar28@gmail.com).
