from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def parse(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # used to make the window wide, since with the narrow one weather desc is hidden and can't be parsed
    options.add_argument("--window-size=1920,1024")
    driver = webdriver.Chrome(options=options)

    forecast = []

    driver.get(url)
    try:
        forecast_element = driver.find_element(By.XPATH, "//article[contains(@class, 'MainPage_appForecast')]")
        day_cards = forecast_element.find_elements(By.TAG_NAME, "a")

        for day_card in day_cards:
            day_block = {
                "date": day_card.find_element(By.XPATH, "article/h3[contains(@style, 'day-title')]").text
            }

            magnetic = ""
            additional_info = day_card.find_elements(By.XPATH, "article/div[contains(@class, 'dayDuration')]/div[contains(@class, 'info')]/div")
            for item in additional_info:
                caption = item.find_element(By.XPATH, "div[contains(@class, 'caption')]").text
                value = item.find_element(By.XPATH, "div[contains(@class, 'value')]").text
                if caption == "Магнитное поле":
                    magnetic = value
            day_block["magnetic"] = magnetic
            
            avg_temp = 0
            day_press = []
            for time_of_day in TimeOfDay:
                tod_key = time_of_day.name
                temp = day_card.find_element(By.XPATH, f"article/div[contains(@style, '{tod_key}-temp')]").text
                press = day_card.find_element(By.XPATH, f"article/div[contains(@style, '{tod_key}-press')]").text

                day_press.append(int(press))

                if tod_key != TimeOfDay.n:
                    avg_temp += int(temp[0:len(temp)-1])

                day_block[tod_key] = {
                    "temp": temp,
                    "press": press,
                    "hum": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{tod_key}-hum')]").text,
                    "weather": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{tod_key}-text')]").text,
                }
            day_block["avg_temp"] = round(avg_temp / 3.0, 1)

            # FEAT: implement corner-case - both growing and dropping of pressure in one day
            press_changing = ""
            press_min = min(day_press)
            press_max = max(day_press)
            if press_max - press_min >= 5:
                if day_press.index(press_min) < day_press.index(press_max):
                    press_changing = "Ожидается резкое увеличение атмосферного давления"
                else:
                    press_changing = "Ожидается резкое падение атмосферного давления"
            day_block["press_changing"] = press_changing
            
            forecast.append(day_block)
    except NoSuchElementException as e:
        print(f"Some element was not found: {e.msg}")

    driver.quit()
    return forecast


class TimeOfDay(Enum):
    m = "Утро"
    d = "День"
    e = "Вечер"
    n = "Ночь"

    def __iter__(self):
        return iter(list(self.m, self.d, self.e, self.n))
