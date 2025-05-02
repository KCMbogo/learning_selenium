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
            print(f"\t\tQuestion {index+1} of {len(questions)}")
            
            question_text= " "

            try:
                try:
                    question_text = question.find_element(by=By.CSS_SELECTOR, value='div[role="heading"]').text
                    print(f"\t\tPrompt: {question_text}")
                except:
                    print("\t\tNo question heading was found...")

                inputs = question.find_elements(by=By.TAG_NAME, value="input")
                textareas = question.find_elements(by=By.TAG_NAME, value="textarea")
                radios = question.find_elements(by=By.CSS_SELECTOR, value="div[role='radio']")
                checkboxes = question.find_elements(by=By.CSS_SELECTOR, value="div[role='checkbox']")
                listboxes = question.find_elements(by=By.CSS_SELECTOR, value="[role='listbox']")

                # TEXT INPUTS
                if inputs:
                    for input_element in inputs:
                        try:
                            WebDriverWait(driver=driver, timeout=10).until(
                                EC.visibility_of(element=input_element)
                            )
                            driver.execute_script("arguments[0].scrollIntoView({ block: 'center' })", input_element)
                            
                            input_type = input_element.get_attribute(name="type")
                            aria_label = input_element.get_attribute(name="aria-label")

                            time.sleep(.5)

                            print(f"\t\t\tFound {len(inputs)} option(s) of type {input_type}")

                            if input_type == "text" and "name" in question_text:
                                answer = random.choice(data["names"])
                                time.sleep(.5)
                                input_element.send_keys(answer)
                                print(f"\t\t\tAnswered: {answer}")
                            elif input_type == "text" and "email" in question_text:
                                answer = random.choice(data["emails"])
                                time.sleep(.5)
                                input_element.send_keys(answer)
                                print(f"\t\t\tAnswered: {answer}")
                            elif input_type == "date":
                                start = datetime(year=1970, month=1, day=1)
                                end = datetime.now() - timedelta(days=365 * 12)
                                random_date = get_random_date(start_date=start, end_date=end)
                                input_element.send_keys(random_date)
                                print(f"\t\t\tAnswered: {random_date}")
                            elif input_type == "number":
                                if aria_label == "Hour":
                                    random_hour = random.randint(0, 23)
                                    input_element.send_keys(random_hour)
                                    print(f"\t\t\tAnswered: {random_hour} hrs")
                                elif aria_label == "Minute":
                                    random_minute = random.randint(0, 59)
                                    input_element.send_keys(random_minute)
                                    print(f"\t\t\tAnswered: {random_minute} min")

                                time.sleep(.5)

                                meridiem = question.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[4]')
                                meridiem.click()
                                time.sleep(.3)
                                meridiem_options = meridiem.find_elements(by=By.CSS_SELECTOR, value="div[role='option']")
                                time.sleep(.3)
                                selected_meridiem = random.choice(meridiem_options)
                                WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of(element=selected_meridiem))
                                selected_meridiem.click()
                                print(f"\t\t\tMeridiem: {selected_meridiem.text}")
                        except:
                            pass
                
                # TEXT AREAS
                elif textareas:
                    textarea = textareas[0] if textareas else None
                    if "experience" in question_text:
                        experience = random.choice(data["experiences"])
                        textarea.send_keys(experience)
                        print(f"\t\t\tAnswered: {experience}")
                    else:
                        pass
                # RADIO BUTTONS
                elif radios:
                    selected_option = random.choice(radios)
                    time.sleep(.3)
                    try:    
                        selected_option.click()
                    except:
                        print("Failed to click radio button")
                        continue
                    print(f"\t\t\tAnswered: {selected_option.get_attribute(name='aria-label')}")
                # CHECKBOXES
                elif checkboxes:
                    num_to_select = random.randint(1, len(checkboxes))
                    random_checkboxes = random.sample(checkboxes, num_to_select)
                    for checkbox in random_checkboxes:
                        if not checkbox.is_selected():
                            checkbox.click()
                        print(f"\t\t\tAnswered: {checkbox.get_attribute(name='aria-label')}")
                # DEOPDOWNS
                elif listboxes:
                    listbox = listboxes[0]
                    listbox.click()
                    time.sleep(.3)
                    options = listbox.find_elements(by=By.CSS_SELECTOR, value="[role='option']")
                    selected = random.choice(options)
                    selected.click()
                    print(f"\t\t\tAnswered:{selected.get_attribute(name='aria-label')}")
                else:
                    print("Unexpected error occured")
                    driver.quit()
            except:
                pass

        # for index, question in enumerate(questions):
        #     print(f"\n\tQuestion {index+1} of {len(questions)}")

        #     question_text = ""
        #     try:
        #         question_text = question.find_element(By.CSS_SELECTOR, 'div[role="heading"]').text
        #         print(f"\t\tPrompt: {question_text}")
        #     except:
        #         print("\t\tNo heading text found.")

        #     inputs = question.find_elements(By.TAG_NAME, "input")
        #     textareas = question.find_elements(By.TAG_NAME, "textarea")
        #     radios = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
        #     checkboxes = question.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
        #     listboxes = question.find_elements(By.CSS_SELECTOR, "div[role='listbox']")

        #     # --- TEXT INPUT ---
        #     if inputs:
        #         for input_element in inputs:
        #             try:
        #                 input_type = input_element.get_attribute("type")
        #                 aria_label = input_element.get_attribute("aria-label")
        #                 print(f"\t\tInput type: {input_type}, Label: {aria_label}")

        #                 if input_type == "text" and "name" in question_text.lower():
        #                     answer = random.choice(data["names"])
        #                     input_element.send_keys(answer)
        #                     print(f"\t\tAnswered: {answer}")
        #                 elif input_type == "text" and "email" in question_text.lower():
        #                     answer = random.choice(data["emails"])
        #                     input_element.send_keys(answer)
        #                     print(f"\t\tAnswered: {answer}")
        #                 elif input_type == "date":
        #                     start = datetime(year=1970, month=1, day=1)
        #                     end = datetime.now() - timedelta(days=365 * 12)
        #                     random_date = get_random_date(start, end)
        #                     input_element.send_keys(random_date)
        #                     print(f"\t\tAnswered: {random_date}")
        #                 elif input_type == "number":
        #                     if "hour" in aria_label.lower():
        #                         hr = random.randint(0, 23)
        #                         input_element.send_keys(hr)
        #                         print(f"\t\tAnswered: {hr} hour(s)")
        #                     elif "minute" in aria_label.lower():
        #                         mn = random.randint(0, 59)
        #                         input_element.send_keys(mn)
        #                         print(f"\t\tAnswered: {mn} minute(s)")
        #             except Exception as e:
        #                 print(f"\t\tInput error: {e}")

        #     # --- TEXTAREA ---
        #     elif textareas:
        #         try:
        #             textarea = textareas[0]
        #             if "experience" in question_text.lower():
        #                 response = random.choice(data["experiences"])
        #                 textarea.send_keys(response)
        #                 print(f"\t\tAnswered: {response}")
        #             else:
        #                 textarea.send_keys("N/A")
        #                 print(f"\t\tDefaulted to: N/A")
        #         except Exception as e:
        #             print(f"\t\tTextarea error: {e}")

        #     # --- RADIO BUTTONS ---
        #     elif radios:
        #         try:
        #             selected = random.choice(radios)
        #             selected.click()
        #             print(f"\t\tSelected: {selected.get_attribute('aria-label')}")
        #         except Exception as e:
        #             print(f"\t\tRadio error: {e}")

        #     # --- CHECKBOXES ---
        #     elif checkboxes:
        #         try:
        #             count = len(checkboxes)
        #             n = random.randint(1, count)  # at least 1
        #             selected = random.sample(checkboxes, n)
        #             for box in selected:
        #                 aria = box.get_attribute("aria-label")
        #                 box.click()
        #                 print(f"\t\tChecked: {aria}")
        #         except Exception as e:
        #             print(f"\t\tCheckbox error: {e}")

        #     # --- DROPDOWN / LISTBOX ---
        #     elif listboxes:
        #         try:
        #             listbox = listboxes[0]
        #             listbox.click()
        #             time.sleep(0.3)
        #             options = driver.find_elements(By.CSS_SELECTOR, "div[role='option']")
        #             if options:
        #                 choice = random.choice(options)
        #                 driver.execute_script("arguments[0].scrollIntoView(true);", choice)
        #                 choice.click()
        #                 print(f"\t\tDropdown selected: {choice.get_attribute('aria-label')}")
        #             else:
        #                 print("\t\tNo options found.")
        #         except Exception as e:
        #             print(f"\t\tDropdown error: {e}")

        #     else:
        #         print("\t\tNo recognized input types.")


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        submit_btn = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')  
        time.sleep(.3)
        if submit_btn:
            try:
                submit_btn.click()
                if "formResponse" in driver.current_url:
                    print(f"Completed submission")
                else:
                    time.sleep(10)
                    print("Failed to submit form")
            except:
                driver.execute_script("arguments[0].click()", submit_btn)
                if "formResponse" in driver.current_url:
                    print(f"Completed submission via JavaScript")
                else:
                    print("Failed to submit form via JavaScript")
        else:
            print("Submit button not found!")
                
    else:
        print(f"No questions found in: {url}")
except Exception as e:
    print(f"Error: {e}")
    driver.quit()


