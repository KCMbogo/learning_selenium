import time
import json
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
# options.add_argument('--start-maximized')
options.add_argument("--lang=en")
prefs = {
    "intl.accept_languages": "en,en_US"
}
options.add_experimental_option("prefs", prefs)
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

url = "https://docs.google.com/forms/d/e/1FAIpQLSdjwAor8jhx7b1AdYkWfc-IvZTHjq9N0S486OzCcBy_aHIJXA/viewform?usp=header"

try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print(f"Failed to open driver: {e}")

# load json data (person objects)
data_path = "data.json"

with open(data_path, "r") as json_file:
    data = json.load(json_file)

def get_random_date(start_date, end_date, date_format="%Y-%m-%d"):
    delta = end_date - start_date
    random_days = random.randint(a=0, b=delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime(date_format)

try:
    driver.get(url=url)
    
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located(locator=(By.CSS_SELECTOR, "form"))
    )

    print('Form Detected.')

    questions = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="Qr7Oae"]')
    if questions:
        print(f"\tFound {len(questions)} questions")

        for index, question in enumerate(questions):
            print(f"\n\tQuestion {index+1} of {len(questions)}")

            try:
                question_text = question.find_element(By.CSS_SELECTOR, 'div[role="heading"]').text
                print(f"\tPrompt: {question_text}")
            except:
                question_text = ""
                print("\tNo heading found.")

            inputs = question.find_elements(By.TAG_NAME, "input")
            textareas = question.find_elements(By.TAG_NAME, "textarea")
            radios = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            checkboxes = question.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            listboxes = question.find_elements(By.CSS_SELECTOR, "[role='listbox']")

            time.sleep(1)

            # --- TEXT INPUTS ---
            for input_element in inputs:
                try:
                    input_type = input_element.get_attribute("type")
                    aria_label = input_element.get_attribute("aria-label") or ""
                    if input_type == "text":
                        if "name" in question_text.lower():
                            answer = random.choice(data["names"])
                        elif "email" in question_text.lower():
                            answer = random.choice(data["emails"])
                        else:
                            answer = "Test input"
                        input_element.send_keys(answer)
                        print(f"\tAnswered: {answer}")

                    elif input_type == "date":
                        date = get_random_date(datetime(1970, 1, 1), datetime.now() - timedelta(days=365*12))
                        input_element.send_keys(date)
                        print(f"\tAnswered: {date}")

                    elif input_type == "number":
                        label = input_element.get_attribute(name="aria-label") or ""
                        label = label.lower()
                        if "saa" == label:
                            hr = random.randint(0, 23)
                            input_element.send_keys(str(hr))
                            print(f"\tHour: {hr}")
                        elif "dakika" == label:
                            min_ = random.randint(0, 59)
                            input_element.send_keys(str(min_))
                            print(f"\tMinute: {min_}")

                except Exception as e:
                    print(f"\tInput error: {e}")

            # --- TEXTAREAS ---
            for textarea in textareas:
                try:
                    answer = random.choice(data["experiences"])
                    textarea.send_keys(answer)
                    print(f"\tTextarea Answered: {answer}")
                except Exception as e:
                    print(f"\tTextarea error: {e}")

            # --- RADIOS ---
            if radios:
                try:
                    choice = random.choice(radios)
                    choice.click()
                    print(f"\tRadio: {choice.get_attribute('aria-label')}")
                except Exception as e:
                    print(f"\tRadio error: {e}")

            # --- CHECKBOXES ---
            if checkboxes:
                try:
                    to_click = random.sample(checkboxes, random.randint(1, len(checkboxes)))
                    for box in to_click:
                        box.click()
                        print(f"\tCheckbox: {box.get_attribute('aria-label')}")
                except Exception as e:
                    print(f"\tCheckbox error: {e}")

            # --- DROPDOWN ---
            if listboxes:
                try:
                    listbox = listboxes[0]
                    listbox.click()
                    time.sleep(.3)
                    options = question.find_elements(By.CSS_SELECTOR, "div[role='option']")
                    valid_options = [
                        option for option in options 
                        if option.text.lower() not in ["select", "choose", "pick one", "select an option"]
                    ]
                    selected = random.choice(valid_options)
                    selected.click()
                    print(f"\tDropdown: {selected.text}")
                except Exception as e:
                    print(f"\tDropdown error: {e}")


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        submit_btn = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')  
        time.sleep(.3)
        if submit_btn:
            try:
                submit_btn.click()
                WebDriverWait(driver=driver, timeout=10).until(
                    EC.url_contains(url="formResponse")
                )
            except:
                driver.execute_script("arguments[0].click()", submit_btn)
                WebDriverWait(driver=driver, timeout=10).until(
                    EC.url_contains(url="formResponse")
                )
            else:
                print("Failed to submit form")
        else:
            print("Submit button not found!")
                
    else:
        print(f"No questions found in: {url}")
except Exception as e:
    print(f"Error: {e}")
    driver.quit()


