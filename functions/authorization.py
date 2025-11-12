import time
import config
import logging
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


def get_random_chrome_user_agent():
    try:
        user_agent = UserAgent(browsers='chrome', os='macos', platforms='pc')
        return user_agent.random
    except Exception as e:
        logger.error(f'Ошибка в получении User-agent: {e}.')


def authorization(login_, password_):
    options = webdriver.ChromeOptions()
    options.add_argument(get_random_chrome_user_agent())
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(config.AUTHORIZATION_URL)
        wait = WebDriverWait(driver, 5)

        login_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_login')))
        login_input = login_input_container.find_element(By.TAG_NAME, 'input')
        login_input.clear()
        login_input.send_keys(login_)
        time.sleep(1)

        pass_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_password')))
        pass_input = pass_input_container.find_element(By.TAG_NAME, 'input')
        pass_input.clear()
        pass_input.send_keys(password_)
        time.sleep(1)

        input_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_login')))
        input_button = input_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        input_button.click()
        time.sleep(5)

        config.MAIN_HTML = BS(driver.page_source, 'html.parser')

        driver.get(config.AUTO_LIST_URL)
        time.sleep(5)
        config.AUTO_HTML = BS(driver.page_source, 'html.parser')

        driver.close()
        driver.quit()
        return True

    except Exception as ex:
        logger.error(f'Ошибка авторизации: {ex}.')
        driver.close()
        driver.quit()
        return False
