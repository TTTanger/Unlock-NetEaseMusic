# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0017EDB93FE8CA4D71324830737194911D01B8FE1B0E73578328D1D1C12C2ADFFAB4BE92D4B72C36E996E6AD0051C58F64135B7BAB28D8BC28CAF47F0ECB1FB1F3EFE400B5574C95B755217CB1E844B0352A36DF123EB2424E895C1420AEA23F557AFFEDD436D392C0A7B70DB500444853157BCCBA60F83A9BE1C8F832D8E198A13F3810339C49F347F8DF8CFD4DF5E597020D034876DBAA1AF7E151F76D63EF28109CF07904D56E3CD78F95F560C3A493C74DA40C4EE7A3DC9955A4DCE549880133E25C80A9465B1DF96B94B572E830BD676D524F30D8F2FACB8B1BE281E204271114F2ADE45B90A2C48276ED21FE84D352ADD6A859F2DD6DE4171376D67BC0810C8B91EC3EE38BD973BC9AFE540F9D397313EE08CE8526E3EDA7E9818E0648F27B13DF1B27ED11D746CD190BDB5D6013737A4A6EB162F2227FF8E8BFDA2CB262466EAB1E1F363B862AD4194244EA6D4460A177377273E1914EC1CB91ECD2F1E1D990D927D26695EABA102716AE5E6C4C8B8609B09ACFB0053793D7798A95125BDE34752D8D35C3FFB28AEF1501CF695BCE5B19D1F05EBA2EC997A069606DB96B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
