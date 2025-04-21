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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AB096E06B454678CD2BDC176463C594EC62B18710AAF474D2785F18C8738C5AC7ACD327EC0C9F0450F5562C06738A4F6FDA8902FE842AA5C1B2323DD7D7ED4D8C0D574DDFBB2787C09E4C185A4640E233923F19A2C71BC8617214A042465F43AA6CD589E64711FE3501B2F177FBCBAB9A25B0048AE1156C6E76B4F4569A74413DAA74887649EF9462398B72822C8DF1F4D446F2754FF0699F8F7A7FE374EACB51A13A77C3191853CE450B08D034434F98B205E7AD193BCA178B063A660F4BCA66AB9828E9931FDADD4C38C692061CA9018C7E46EADE771FFC33B5D5949CE1747E72D9BE3CC3AE47655BB926968F5097CB1FCF21BA748F351398296430DB3C60379C971781650E807324865CCB34E2241331797AAEA13FBFD8206D014EFA13B7AF53E591AAF2CDCFE00EF9ADBC25DD0BA2F6A30D042AB443C16FCE5FF6A5C2EBF124747941AD73923B4541D47890CA345D7EC783BCCA8353F2FEF315440D00770"})
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
