from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import credentials
import argparse

def getStatus(UNIQUE_ID):

    login_url = f'https://utdirect.utexas.edu/apps/registrar/course_schedule/20249/{UNIQUE_ID}/'
    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.set_window_size(580,490)


    time.sleep(2)

    username_field = driver.find_element(by=By.ID, value="username")
    username_field.click()
    username_field.send_keys(credentials.USERNAME)
    password_field = driver.find_element(by=By.ID, value="password")
    password_field.click()
    password_field.send_keys(credentials.PASSWORD)
    password_field.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 60)

    button_locator = (By.TAG_NAME, "button")
    #button_field = driver.find_element(by=By.TAG_NAME, value="button")
    button_field = wait.until(EC.element_to_be_clickable(button_locator))
    button_field.click()

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
        #notifyUser("Registration Alert", f"class with unique id {UNIQUE_ID} is now open", credentials.API_KEY)
        time.sleep(10)
        driver.refresh()
        # now at webpage.

def notifyUser(title, body, api_key):
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {'Access-Token': api_key}
    data = {
        'type': 'note',
        'title': title,
        'body': body
    }
    response = requests.post(url, headers=headers, json=data)
    if (response.status_code == 200):
        print('success')

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
    args = parser.parse_args()
    getStatus(args.UNIQUE_ID)
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