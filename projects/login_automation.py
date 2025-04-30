import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

options = Options()

options.add_argument("--start-maximized")
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)

driver = Chrome(options=options)

try:
    driver.get(url="https://the-internet.herokuapp.com/login")
except Exception as e:
    print(f"Failed to get url: {e}")

time.sleep(2)

try:
    username_field = driver.find_element(by=By.NAME, value="username")
    pwd_field = driver.find_element(by=By.NAME, value="password")
    submit = driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')

    if username_field or pwd_field:
        username_field.send_keys("tomsmith")
        pwd_field.send_keys("SuperSecretPassword!")

        try:
            submit.click()
            time.sleep(1)
            success = driver.find_element(by=By.CLASS_NAME, value="success")
            if success:
                print(f"Message: {success.text}")
                current_url = driver.current_url
                print(f"Current URL: {current_url}")
                print(f"Webpage content:\n {driver.page_source}")

                prompt = input("Press Enter to quit or type 'logout' to Logout:\t")
                if prompt.lower() == 'logout':
                    logout_btn = driver.find_element(by=By.CLASS_NAME, value="button")
                    if logout_btn:
                        try:
                            logout_btn.click()
                        except:
                            driver.execute_script("arguments[0].click();", logout_btn)
                    else:
                        print("No logout button found!")
                else:
                    print("Quiting browser...")
        except:
            driver.execute_script("arguments[0].click();", submit)

except Exception as e:
    print(f"Error: {e}")
    driver.quit()

