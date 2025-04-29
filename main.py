from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# NOTE: A SIMPLE SELENIUM SCRIPT TO SEARCH IN CHROME

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(10)

try:
    print("Getting url")
    # navigate to url
    driver.get("https://www.google.com")

    print("Got url")

    # locate and use searchbox
    search_box = driver.find_element(by=By.NAME, value="q")
    search_box.send_keys("Kadilana Mbogo")
    search_box.send_keys(Keys.RETURN)
    print("Searching........")

    # wait and click first result
    time.sleep(2)
    first_result = driver.find_element(by=By.CSS_SELECTOR, value='h3')
    print("Found element")
    first_result.click()
    print("Clicked")
    time.sleep(3)
except Exception as e:
    print(f"Error: {e}")
    driver.quit()