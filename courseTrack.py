from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import easygui
import credentials
import argparse

def getStatus(UNIQUE_ID, FALL, YEAR, show_gui, refresh_interval):

    login_url = f'https://utdirect.utexas.edu/apps/registrar/course_schedule/{YEAR}{9 if FALL else 2}/{UNIQUE_ID}/'
    options = Options()
    if not show_gui: # optional switch to display chrome browser
        options.add_argument('--headless')

    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options)
    
    print('Authenticating...')
    
    driver.get(login_url)
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
    button_field = wait.until(EC.element_to_be_clickable(button_locator))
    button_field.click()

    print('###### Course Tracker Log ######')
    print('PLEASE AUTHENTICATE WITH DUO MOBILE')

    button_field = wait.until(EC.element_to_be_clickable(button_locator))
    button_field.click()

    time.sleep(3)
    driver.minimize_window()

    last_status = None

    while (True):
        className = driver.find_elements(by=By.TAG_NAME, value="h2")[0].text
        matches = driver.find_elements(by=By.TAG_NAME, value="td")
        cur_status = [ x for x in matches if 
            x.text == "waitlisted" or 
            x.text == "open" or 
            x.text == "open; reserved" or 
            x.text == "closed"
        ][0].text

        if (refresh_interval):
            SLEEP_TIME = refresh_interval
        else:
            SLEEP_TIME = 10 # default is 10 sec

        if (cur_status == last_status):
            print(f"Unique ID {UNIQUE_ID} is still {last_status}.")
            time.sleep(SLEEP_TIME)
            driver.refresh()
            continue
        else:
            if (cur_status == "closed"):
                print(f"{className} with unique ID {UNIQUE_ID} is currently " + cur_status)
            elif cur_status == "cancelled":
                print(f"{className} with unique ID {UNIQUE_ID} is cancelled for {YEAR}.")
                exit(0)
            else:
                notifyUser(f"{className} with unique id {UNIQUE_ID} is now {cur_status}!")
        
        last_status = cur_status
        time.sleep(SLEEP_TIME)
        driver.refresh()

def notifyUser(body):
    userIn = easygui.ynbox(body + "\nWould you like to go to the registration page?", "courseTrack", ("Yes", "No"))
    if (userIn):
        goToRegistrationPage(webdriver)
        
def goToRegistrationPage(webdriver):
    # TODO
    return 0
        
def main():
    parser = argparse.ArgumentParser(description="Script to periodically check if a current UT course is CLOSED, OPEN, RESERVED, or WAITLISTED. Please invoke the script with the first argument being the course's unique ID number.\n\nEX: python courseTrack.py 50700\n\n")
    parser._action_groups.pop()
    required = parser.add_argument_group('Required')
    optional = parser.add_argument_group('Optional')
    required.add_argument('UNIQUE_ID', type=int, help='The 5-digit unique course code')
    required.add_argument('SEASON', type=str, help='Fall, spring, or summer')
    required.add_argument('YEAR', type=int, help='Current academic year')
    optional.add_argument("--show-gui", help = 'Switch to display the selenium chrome driver, usually for debugging.', action="store_true")
    optional.add_argument("--refresh-interval", type=int, help="""
                          Time (sec) between each refresh.
                                    # CAUTION #  
                          Rate limiting may occur when the 
                          interval is set to a value < 2.""")
    args = parser.parse_args()

    isFall = args.SEASON.upper() == 'FALL'
    getStatus(args.UNIQUE_ID, isFall, args.YEAR, args.show_gui, args.refresh_interval)


if __name__ == "__main__":
    main()