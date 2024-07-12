from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Safari()

try:
    driver.get("http://127.0.0.1:5000")

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys("john@simplylift.co")
    time.sleep(2)

    enter_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    time.sleep(2)

    enter_button.click()
    time.sleep(2)

    book_places_link = driver.find_element(By.CSS_SELECTOR, "a[href='/book/Spring%20Festival/Simply%20Lift']")
    book_places_link.click()
    time.sleep(2)

    number_field = driver.find_element(By.NAME, "places")
    number_field.send_keys(1)
    time.sleep(2)

    book_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    book_button.click()
    time.sleep(2)

    logout_link = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
    logout_link.click()
    time.sleep(2)

finally:
    driver.quit()
