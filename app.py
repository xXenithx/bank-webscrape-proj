from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from configparser import ConfigParser
import time

def StartUp():
    parser = ConfigParser()
    parser.read('app.config')

    WINDOW_SIZE = parser.get('chrome-webdriver', 'windowSize')
    LOG_LEVEL = parser.get('chrome-webdriver', 'logLevel')
    CHROME_PATH = parser.get('chrome-webdriver', 'chromePATH')
    DOWNLOAD_DIR = parser.get('chrome-webdriver', 'downloadDir')
    
    USERNAME = parser.get("bank-login", "username")
    PASSWORD = parser.get("bank-login", "password")

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument(LOG_LEVEL)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(options=chrome_options)
    
    enable_download_in_headless_chrome(driver, DOWNLOAD_DIR)

    grab_site(driver, USERNAME, PASSWORD)

def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir }}
    command_result = driver.execute("send_command", params)
    print('[Info]')
    print(command_result)

def grab_site(driver, username, password):
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.gecu.com")
    print("\nNow fetching from https://www.gecu.com")
    # cur_url = driver.current_url
    
    driver.find_element_by_name('header_0$login_0$userid_login').send_keys(username)
    driver.find_element_by_name('header_0$login_0$realpassword').send_keys(password)
    driver.find_element_by_id('signin_button').click()

    wait.until(EC.title_is('G E C U | Authentication'))
    # print("Now current url is at: " + driver.current_url)

    if driver.title == 'G E C U | Authentication':
        print("\nPassword correct, now waiting for authentication.")
        wait.until(EC.presence_of_element_located((By.NAME, "sendOTP")))
        driver.find_element_by_name('sendOTP').click()

        code = input("Please Enter 6 Digit Access Code:")
        driver.find_element_by_name('mfaCodeInputField').send_keys(code)
        driver.find_element_by_name('registerDevice').click()

        wait.until(EC.title_is('G E C U | Home'))

    if driver.title == 'G E C U | Home':
        wait.until(EC.presence_of_element_located((By.ID, "accountNumberCtfLpgOiAV2ST6Xj0a01dBcMII349MJ1Oc02FC1vtvY")))
        driver.find_element_by_id('accountNumberCtfLpgOiAV2ST6Xj0a01dBcMII349MJ1Oc02FC1vtvY').click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_15uqqS2z-k0c038a03baNN")))
        driver.find_element_by_class_name('_15uqqS2z-k0c038a03baNN').click()

        wait.until(EC.presence_of_element_located((By.ID, "exportFile")))

        driver.find_element_by_id('exportFile').click()
        print("Successfully downloaded Monthly Bank Statement")
        time.sleep(3)

    else:
        print('Error: could not find the right page!')

    driver.close()

if __name__ == "__main__":
    StartUp()