import json

import parse_with_selenium

if __name__ == "__main__":
    # static for testing purposes
    # TODO: should be generated depending on input city later on
    url = "https://yandex.ru/pogoda/ru?lat=59.938784&lon=30.314997"

    forecast = parse_with_selenium.parse(url)

    print(json.dumps(forecast, indent=4, ensure_ascii=False))
