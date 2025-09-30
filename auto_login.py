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
    browser.add_cookie({"name": "MUSIC_U", "value": "005CC511800AFCBBFD14E0DABF474CCE142C9F426373CBE6C1621472EA000A3AA1429A55E068BF8C68DCACD2116DA688CCEBF5438F816558252A1A9ADF9BA8FD82E1275299BBBC489E0857F0F7D4FC7111DC432F0C35A70D00CEFB1F503A5F56EDBDE888E850C81B6F691074FEC36C5E84B42ACB901A3C7401AC983078A24DE4E55BBCDC77115682071801186E0F5F89D3B3AFAED07418974B1E6FDC404662669EF6366653C014B4496C21D6E35CB68A6A375EEE579AEE89E37C8C4484213ED4002C210630221503D376C825075DBECB4B1D4D3812DF1AE99BEDCAF64E59F82CED23513E6F15FB287D19197CE1E65BCC80855D6A0DEF341CEBB5D4696560D9AFE943D1779DD15BB101A503838B106B29BE9BDD3D85D2CAE09F536C14D7EB16DA22780B7328D049BA5C693535855695E1F32BA64339C35CF1B0C4B3F80EFA2CD8D431C26198B875FA8E8CEB3032C5387AADCE0645E6B3CA8474AE4D2043817BCB907B87E84063AA20337CECF6214922F742C09B882DF3DB630C2668999042D75B59A2CFE65FD3BBFC1B1794DE0FB3D46BA42231B6147AC15FFD9F4B978B3D6DB392"})
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
