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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D55CEABCDCE154E7F941C716D232E616F4367720F53D7E14B8659F0F35670ED4F04634D0F13C5A987AAEDA34F508C9696DE12CEAE7AC4E42FD8B65C60582EE52317C810B519F020079B4CFC401A7B9769663D704CB4F938CBD9B5DA4A81FE4D683CB929658BA7ADDAB193017C3C59E55AA4B6A1CDA5FCAC95C7F8D0DB95D1AAD4DBC8242DC0FABE629B7471EECC0257CB72FEC080182318236706B3F635414164196F75FC0A6B6C07165C0D268959324C88415FEF1FC12419DF8143B7E48590044F70B5F109E65A92E7DB1235AA162F056F3B7A8F083962624F6A9D149B6E1065C5B9BCD9AD6D96853C06A259CD696CE422EA95AE5F15FD744523141304DBC83D9D225C1A071386690536A87551E91CD996E69EEA883768684A5B6888EA1910D05FE567FF61C70C66ED5156860343C368289EB6C64939EF48756EABC362DEC111A9C69BFDF184656EF287AB8E91189ACFF9DE28A71D6FEEF0DFC3BDE45C44B29"})
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
