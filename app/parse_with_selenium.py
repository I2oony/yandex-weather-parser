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
        forecast_element = driver.find_element(By.CSS_SELECTOR, "article[class^='MainPage_appForecast']")
        day_cards = forecast_element.find_elements(By.TAG_NAME, "a")

        for day_card in day_cards:
            day_block = {
                "date": day_card.find_element(By.XPATH, "article/h3[contains(@style, 'day-title')]").text
            }

            for time_of_day in TimeOfDay:
                day_block[time_of_day.value] = {
                    "temp": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{time_of_day.value}-temp')]").text,
                    "press": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{time_of_day.value}-press')]").text,
                    "hum": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{time_of_day.value}-hum')]").text,
                    "weather": day_card.find_element(By.XPATH, f"article/div[contains(@style, '{time_of_day.value}-text')]").text,
                }
            
            forecast.append(day_block)
    except NoSuchElementException as e:
        print(f"Some element was not found: {e.msg}")

    driver.quit()
    return forecast


class TimeOfDay(Enum):
    MORNING = "m"
    DAY = "d"
    EVENING = "e"
    NIGHT = "n"

    def __iter__(self):
        return iter(list(self.MORNING, self.DAY, self.EVENING, self.NIGHT))
