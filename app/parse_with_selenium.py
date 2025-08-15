from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def parse(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    # driver.implicitly_wait(10)

    driver.get(url)
    try:
        forecast = driver.find_element(By.CSS_SELECTOR, "article[class^='MainPage_appForecast']")
        day_cards = forecast.find_elements(By.TAG_NAME, "a")

        for day_card in day_cards:
            day = day_card.find_element(By.XPATH, "article/h3[contains(@style, 'day-title')]")
            
            # morning
            m_temp = day_card.find_element(By.XPATH, "article/div[contains(@style, 'm-temp')]")
            m_press = day_card.find_element(By.XPATH, "article/div[contains(@style, 'm-press')]")
            m_hum = day_card.find_element(By.XPATH, "article/div[contains(@style, 'm-hum')]")

            # FIXME: won't work - no text displayed ???
            weather_type = day_card.find_element(By.XPATH, "article/div[contains(@style, 'text')]")
            print(f"weather_type={str(weather_type)}")

            # day
            d_temp = day_card.find_element(By.XPATH, "article/div[contains(@style, 'd-temp')]")
            d_press = day_card.find_element(By.XPATH, "article/div[contains(@style, 'd-press')]")
            d_hum = day_card.find_element(By.XPATH, "article/div[contains(@style, 'd-hum')]")

            # evening
            e_temp = day_card.find_element(By.XPATH, "article/div[contains(@style, 'e-temp')]")
            e_press = day_card.find_element(By.XPATH, "article/div[contains(@style, 'e-press')]")
            e_hum = day_card.find_element(By.XPATH, "article/div[contains(@style, 'e-hum')]")

            # nigth
            n_temp = day_card.find_element(By.XPATH, "article/div[contains(@style, 'n-temp')]")
            n_press = day_card.find_element(By.XPATH, "article/div[contains(@style, 'n-press')]")
            n_hum = day_card.find_element(By.XPATH, "article/div[contains(@style, 'n-hum')]")

            print(day.text)
            print(f"{m_temp.text} -- {m_press.text} -- {m_hum.text} -- {weather_type.text}")
            print(f"{d_temp.text} -- {d_press.text} -- {d_hum.text} -- {weather_type.text}")
            print(f"{e_temp.text} -- {e_press.text} -- {e_hum.text} -- {weather_type.text}")
            print(f"{n_temp.text} -- {n_press.text} -- {n_hum.text} -- {weather_type.text}")
    except NoSuchElementException as e:
        print(f"Some element not found: {e.msg}")


    # driver.quit()
