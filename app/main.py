# import parse_with_requests
import parse_with_requests_html

if __name__ == "__main__":
    # static for testing purposes
    # TODO: should be generated depending on input city later on
    url = "https://yandex.ru/pogoda/ru?lat=59.938784&lon=30.314997"

    # parse_with_requests.save_page(url, "tmp/example_01.html")
    parse_with_requests_html.save_page(url, "tmp/example_02.html")
