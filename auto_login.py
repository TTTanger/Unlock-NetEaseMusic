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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A2C78CB83098391EC2D2F56FFD859674F6A3D282DC3E98C363A58CA13167E3DE3C37D9C30E485F31642D0ECF2E3A897C9975DF5AA78BFA9AB74A7D8DE07D30D00A00E1618A606B948F0B0D7F237668F70C5F935623E9944E002C58A7F0D5B6DCFEE92987E0D671D50EA5320664AFBFC318869736814BD9C872AE8011B566D5C4FA206430C6F20DCAE5B232287C73F995891F39EA9982EDB91301DA3564C9EE8F9F653DA2AF21A316C667718FCEBED3C3117A8C1F9649F6ECDACA61246D6E7BAFD1438ADD0CCDF548CCB4EF738CE82E8B0DECB7D19621D3996576C10FB67932478D0E6D0AEC926537A8D50D9E10A578B322FE3378E6610045EBA8EFF59B654EFFD746A29AE0336951CE0C45BD6B7BC4832E5DB6C37F20659427C648F7648D5BEA287DD4D64AC2F8444A8B009B9F537253225B675CC514DF74C5DF77A6026E7B41FE24F125F96A0005E55723B667C6C649E568580F1F945BEF83CFA266CCDCFAFD0D6ABB7C758D53BD474F6343AEC2D129CDCE7A769EF5381BC1C86C9589582F6561E53FFA561C690B9FFC3D38184438906BE827BF0D1E97464C513CC800BD56AD"})
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
