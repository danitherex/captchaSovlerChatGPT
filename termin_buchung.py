from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import json
from captcha import get_captcha_code
from uploadImage import upload_image_from_base64

from airflow.models import Variable

load_dotenv(".env",override=True)

#sport_email = os.getenv("SPORT_EMAIL")
#sport_password = os.getenv("SPORT_PASSWORD")
#sport_url = os.getenv("SPORT_URL")
#_captcha = os.getenv("CAPTCHA")

sport_email = Variable.get("SPORT_EMAIL")
sport_password = Variable.get("SPORT_PASSWORD")
sport_url = Variable.get("SPORT_URL")
_captcha = Variable.get("CAPTCHA")

captcha = _captcha.lower() == "true"

#target_weekday_time = json.loads(os.getenv("WEEKDAYS"))
target_weekday_time = json.loads(Variable.get("WEEKDAYS"))


def sign_up():

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    driver.get(sport_url)
    
    original_window = driver.current_window_handle
    
    
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody > tr")

    row = retrieve_row(rows)
    
    
    if(row == None):
        print("No free slots available")
        return
    try:
        try:
            # Close or accept the cookie notice
            cookie_notice_accept_button = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cookie-reject:nth-child(3)")))
            cookie_notice_accept_button.click()
        except Exception as e:
            print("Cookie notice not found or could not be closed.", str(e))
        buchenBtn = WebDriverWait(row, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bs_btn_buchen")))

        buchenBtn.click()
        
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        for window in windows:
            if window != original_window:
                driver.switch_to.window(window)
                break
        
        row = driver.find_element(By.CLASS_NAME, "bs_form_row.bs_rowstripe0")
        weekDay = row.find_element(By.CLASS_NAME,"bs_tag.alr").text
        timeOfDate = row.find_element(By.CLASS_NAME,"bs_time").text
        
        standardizedTimeOfDate = timeOfDate.replace('.', ':')
        
        for _target_weekday, target_time in target_weekday_time.items():
            target_weekday = _target_weekday
            target_time = target_time
            if(weekDay == target_weekday and standardizedTimeOfDate == target_time):
                buchenBtn = WebDriverWait(row, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "inlbutton.buchen")))
                buchenBtn.click()
                
                openPasswordField = driver.find_element(By.ID, "bs_pw_anmlink")
                openPasswordField.click()
                
                emailInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bs_pw_anm > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)")))
                paswordInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bs_pw_anm > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)")))
                continueButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.bs_form_foot:nth-child(5) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)")))
                
                emailInput.send_keys(sport_email)
                paswordInput.send_keys(sport_password)
                
                continueButton.click()
                
                read_checkmark = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bs_bed > label:nth-child(1) > input:nth-child(1)")))
                read_checkmark.click()
                
                continueButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bs_submit")))
                continueButton.click()
                if(captcha):
                    #Captcha handling here
                    captcha_base64_image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.width100"))).get_attribute("src")
                    captcha_url = upload_image_from_base64(captcha_base64_image)
                    captcha_code = get_captcha_code(captcha_url)
                    captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BS_F_captcha")))
                    captcha_input.send_keys(captcha_code)
                    print(captcha_code)               
                
                binding_booking = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bs_right > input:nth-child(1)")))
                binding_booking.click()
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bs_form_main > div.bs_form_row.bs_exspace > div.bs_text_red.bs_text_big")))
                    print("Booking failed")
                    if(captcha):
                        try:
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "NONEXISITANT")))
                            #sign_up()
                        except Exception as e:
                            print("Booking successful")
                except Exception as e:
                    print("Booking successful")

                break      
    except TimeoutException as e:
        print("There seems not to be any free slots available")
    except IndexError as e:
        sign_up()
    except Exception as e:
        print("An error occured: ", str(e))
        raise e
        
    driver.quit()

def retrieve_row(rows):
    for row in rows:
        time = row.find_element(By.CSS_SELECTOR, ".bs_szeit").text
        weekday = row.find_element(By.CSS_SELECTOR, ".bs_stag").text
                
        for _target_weekday, target_time in target_weekday_time.items():
            target_weekday = _target_weekday
            target_time = target_time
            if time == target_time and weekday == target_weekday:
                return row
        
if __name__ == "__main__":
    sign_up()