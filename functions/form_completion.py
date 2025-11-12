import time
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from authorization import get_random_chrome_user_agent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fill_the_form(login_, password_):
    options = webdriver.ChromeOptions()
    options.add_argument(get_random_chrome_user_agent())
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(config.AUTHORIZATION_URL)
        wait = WebDriverWait(driver, 5)

        login_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_login')))
        login_input = login_input_container.find_element(By.TAG_NAME, 'input')
        login_input.clear()
        login_input.send_keys(login_)

        pass_input_container = wait.until(EC.presence_of_element_located((By.ID, 'txt_password')))
        pass_input = pass_input_container.find_element(By.TAG_NAME, 'input')
        pass_input.clear()
        pass_input.send_keys(password_)
        time.sleep(3)

        input_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_login')))
        input_button = input_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        input_button.click()
        time.sleep(3)

        form_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_create_request')))
        form_button = form_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_._3oLjlNg_')
        form_button.click()
        time.sleep(3)

        auto_target_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'lyt_car')))
        auto_target_container.click()
        auto_target = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='_1ewnVtMF']")))
        auto_target.click()
        time.sleep(1)

        auto_target_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lyt_step_trailer')))
        auto_target_container.click()
        auto_target = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='_1ewnVtMF' and contains(text(), 'AB660639')]")))
        auto_target.click()
        time.sleep(1)

        next_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_step_next')))
        next_button = next_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        next_button.click()
        time.sleep(3)

        trans_type_target_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lyt_transportation')))
        trans_type_target_container.click()
        trans_type = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='_1ewnVtMF' and contains(text(), 'Экспорт')]")))
        trans_type.click()
        time.sleep(1)

        kind_type_target_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lyt_kind')))
        kind_type_target_container.click()
        kind_type = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='_1ewnVtMF' and contains(text(), 'Перевозка грузов')]")))
        kind_type.click()
        time.sleep(1)

        checkbox_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'chk_copy')))
        checkbox_input = checkbox_container.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox_input)
        time.sleep(1)

        next_button_container = wait.until(EC.presence_of_element_located((By.ID, 'btn_step_next')))
        next_button = next_button_container.find_element(By.CLASS_NAME, '_1YUb7Yf_')
        next_button.click()
        time.sleep(3)

        # captcha_button_container = wait.until(EC.presence_of_element_located((By.ID, 'lyt_captcha')))
        # captcha_button = captcha_button_container.find_element(By.CSS_SELECTOR, "input[type='hidden']")
        # driver.execute_script("arguments[0].click();", captcha_button)
        # time.sleep(3)

        driver.close()
        driver.quit()
        return True

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        return False
