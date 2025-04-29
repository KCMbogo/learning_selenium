import tempfile
import shutil
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
service = Service(executable_path="/usr/bin/chromedriver")

org_profile = "/home/kadilana/.config/google-chrome/Profile 4"

temp_profile_path = tempfile.mkdtemp()
shutil.copytree(src=org_profile, dst=os.path.join(temp_profile_path, "Profile 4"))

options.add_argument(f"user-data-dir={temp_profile_path}")
options.add_argument("profile-directory=Profile 4")
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options, service=service)

try:
    driver.get("https://www.duckduckgo.com")

    time.sleep(10)

    try:
        search_box = WebDriverWait(driver=driver, timeout=10).until(
            method=EC.presence_of_element_located((By.NAME, "q"))
        )
    except NoSuchElementException as e:
        print(f"Error, no such element found: {e}")
        driver.quit()

    query = input("Enter the search query:\t")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    try:
        results = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
        )

        print(f"There are: {len(results)} results")

        results = results[:5]

        if results:
            for i, result in enumerate(results, 1):
                anchor_tag = result.find_element(by=By.TAG_NAME, value="a").get_attribute(name="href")
                print(f"Result: {i}\n Title: {result.text}\n Link: {anchor_tag}\n")
        else:
            print("No result returned!")
            driver.quit()
    except NoSuchElementException as e:
        print(f"Error, no such element(s) found: {e}")

except Exception as e:
    print(f"Failed to open url: {e}")
    driver.quit()



