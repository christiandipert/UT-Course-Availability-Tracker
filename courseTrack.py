from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import vonage
import requests
import time
import credentials
import argparse

def getStatus(UNIQUE_ID, FALL, YEAR):

    if FALL:
        login_url = f'https://utdirect.utexas.edu/apps/registrar/course_schedule/{YEAR}9/{UNIQUE_ID}/'
    else:
        login_url = f'https://utdirect.utexas.edu/apps/registrar/course_schedule/{YEAR}2/{UNIQUE_ID}/'


    headless = True
    options = Options()

    if headless: # optional switch
        options.add_argument('--headless')

    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options)
    
    driver.get(login_url)
    driver.set_window_size(580,490)
    wait = WebDriverWait(driver, 60)

    usernameLocate = (By.ID, "username")
    passwordLocate = (By.ID, "password")

    username_field = wait.until(EC.presence_of_element_located(usernameLocate))
    username_field.click()
    username_field.send_keys(credentials.USERNAME)

    password_field = wait.until(EC.presence_of_element_located(passwordLocate))
    password_field.click()
    password_field.send_keys(credentials.PASSWORD)
    password_field.send_keys(Keys.RETURN)

    button_locator = (By.TAG_NAME, "button")
    #button_field = driver.find_element(by=By.TAG_NAME, value="button")
    button_field = wait.until(EC.element_to_be_clickable(button_locator))
    button_field.click()

    print('###### Course Tracker Log ######')
    print('PLEASE AUTHENTICATE WITH DUO MOBILE')

    #button_field = driver.find_element(by=By.TAG_NAME, value="button")
    button_field = wait.until(EC.element_to_be_clickable(button_locator))
    button_field.click()

    time.sleep(3)
    driver.minimize_window()

    while (True):
        matches = driver.find_elements(by=By.TAG_NAME, value="td")
        cur_status = [ x for x in matches if 
            x.text == "waitlisted" or 
            x.text == "open" or 
            x.text == "open; reserved" or 
            x.text == "closed"
        ][0].text
        
        if (cur_status != "open" or cur_status != "open; reserved"):
            print(f"Unique ID {UNIQUE_ID} is currently " + cur_status)
        
        notifyUser(f"Registration Alert: class with unique id {UNIQUE_ID} is now waitlisted")
        time.sleep(10)
        driver.refresh()
        # now at webpage.

def notifyUser(body):
    client = vonage.Client(key="7b165c49", secret="DqeAk2K5SU33piBk")
    sms = vonage.Sms(client)
    responseData = sms.send_message({
        "from": "12393427850",
        "to": "18178998688",
        "text": body
    })


'''
def getClassStatus(UNIQUE_ID):
    classOpen = getStatus(UNIQUE_ID)
    if (classOpen):
        notifyUser("Registration Alert", f"class with unique id {UNIQUE_ID} is now open", my_api_key)
    else:
        print('class is still closed')
'''

def main():

    parser = argparse.ArgumentParser(description="Script to periodically check if a current UT course is CLOSED, OPEN, RESERVED, or WAITLISTED. Please invoke the script with the first argument being the course's unique ID number.\n\nEX: python courseTrack.py 50700\n\n")
    parser.add_argument('UNIQUE_ID', type=int, help='The 5-digit unique course code')
    parser.add_argument('SEASON', type=str, help='Fall, spring, or summer')
    parser.add_argument('YEAR', type=int, help='Current academic year')
    args = parser.parse_args()

    isFall = args.SEASON.upper() == 'FALL'
    getStatus(args.UNIQUE_ID, isFall, args.YEAR)

'''
# get next 8am
def get_next_8am():
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    next_8am = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 8, 0)
    return next_8am

# wait until next 8am
def wait_until_next_8am():
    next_8am = get_next_8am()
    time_to_wait = (next_8am - datetime.datetime.now()).total_seconds()
    print(f"Waiting until {next_8am}...")
    time.sleep(time_to_wait)
'''        
if __name__ == "__main__":
    main()