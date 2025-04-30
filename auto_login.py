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
    browser.add_cookie({"name": "MUSIC_U", "value": "0011474B7C4F883B9867BE9F1305A678B3D617CB0BCB9E27BA8EF5C6C2DBFDB61F777FA09297A1EB9960CD3E93E2DE16880C6CC3F652A525F5838BA06CB3D8A2594F9381CA5F6E81CC492043E44E24CA740592C06A9D200142C700FB4A3A3748BDCE0AF84C6C6DE482813E3F33DDECD3F4A0F090756BCAB68B0CFD015AC55B3110F10D836B0A44BD4A3E012A6CAE874578AFAA842AFEF034E5C5C1857905FBBE0458AE778DB86338A6058A60E84E2ACEB07BB5FD2185078EF839640DF62F0C701F5E9A35D443FE89C26E005668D226170E0BD84D9B41955D3E2D531553CB8B3ECE6596E6D2DD2051A76AE771A4955A9C204307395BC3F04511610307A1355906430C8F74F8D9138813FE7491ED4DDB31BE54EE2209E5976D98C816546E608E4D84E8CD870D2EF133D9D724F2FBACDB971E4D1FC72607DF6FFE368FDCAD1725673465DC05BE2B6D1B5A154208C68880C01C460383E370CBA41FCF7F5B800664CD56"})
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
