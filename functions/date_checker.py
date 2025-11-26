import time
import asyncio
import logging
from datetime import datetime, timedelta
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- WebDriver --------------------
def _remote_driver():
    selenium_url = "http://selenium:4444/wd/hub"
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-webrtc")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    chrome_options.page_load_strategy = 'eager'

    for i in range(5):
        try:
            driver = Remote(command_executor=selenium_url, options=chrome_options)
            driver.set_page_load_timeout(60)
            return driver
        except Exception:
            logger.warning(f"Selenium ещё не готов, попытка {i+1}/5")
            time.sleep(2)

    logger.error("Selenium так и не поднялся.")
    return None

# -------------------- CAPTCHA --------------------
def try_solve_recaptcha_checkbox(driver, timeout=12) -> bool:
    logger.info("🧩 Ищем iframe reCAPTCHA...")

    iframe = None
    iframe_locators = [
        (By.XPATH, "//iframe[contains(@src,'recaptcha')]"),
        (By.XPATH, "//iframe[contains(@title,'recaptcha')]"),
        (By.CSS_SELECTOR, "iframe[src*='recaptcha']"),
        (By.CSS_SELECTOR, "iframe[title*='recaptcha']"),
    ]

    # Пробуем все локаторы
    for locator in iframe_locators:
        try:
            iframe = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            break
        except Exception:
            continue

    if iframe is None:
        logger.warning("⚠ reCAPTCHA iframe НЕ найден, но он должен быть! Ошибка загрузки страницы.")
        return False

    try:
        driver.switch_to.frame(iframe)

        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )

        logger.info("🟢 Кликаем по чекбоксу reCAPTCHA")
        driver.execute_script("arguments[0].click();", checkbox)

        def _checked(d):
            checked = checkbox.get_attribute("aria-checked")
            cls = checkbox.get_attribute("class") or ""
            return checked == "true" or "recaptcha-checkbox-checked" in cls

        WebDriverWait(driver, 12).until(_checked)

        logger.info("✅ reCAPTCHA пройдена")
        driver.switch_to.default_content()
        return True

    except Exception as e:
        logger.warning(f"❌ Не удалось пройти reCAPTCHA: {e}")
        try:
            driver.switch_to.default_content()
        except:
            pass
        return False

# -------------------- Выбор даты --------------------
def select_today_in_calendar(driver):
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_month_name = today.strftime("%B").strip()
    today_year = str(today.year)

    # ---------------- открыть календарь ----------------
    try:
        cal_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[contains(@aria-label,'Choose Date')] | //calendaricon | //button[.//svg and contains(@class,'p-icon-wrapper')]")
            )
        )
        driver.execute_script("arguments[0].click();", cal_btn)
        logger.info("📅 Открыт календарь")
        time.sleep(0.5)
    except Exception as e:
        logger.error(f"Не удалось открыть календарь: {e}", exc_info=True)
        return False

    # ---------------- получить текущий месяц и год ----------------
    try:
        month_el = driver.find_element(By.XPATH,
                                       "//div[contains(@class,'p-datepicker-title')]/button[contains(@class,'p-datepicker-month')]")
        year_el = driver.find_element(By.XPATH,
                                      "//div[contains(@class,'p-datepicker-title')]/button[contains(@class,'p-datepicker-year')]")
        displayed_month = month_el.text.strip()
        displayed_year = year_el.text.strip()
        logger.info(f"Текущий месяц в календаре: {displayed_month}, год: {displayed_year}")
    except Exception as e:
        logger.error(f"Не удалось получить текущий месяц/год: {e}", exc_info=True)
        return False

    # ---------------- переключаем на предыдущий месяц, если нужно ----------------
    if displayed_month != today_month_name or displayed_year != today_year:
        try:
            prev_btn = driver.find_element(By.XPATH, "//button[contains(@class,'p-datepicker-prev')]")
            driver.execute_script("arguments[0].click();", prev_btn)
            logger.info("⬅ Переключили на предыдущий месяц")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Не удалось нажать Previous Month: {e}", exc_info=True)
            return False

    # ---------------- выбираем сегодняшний день ----------------
    try:
        today_el = driver.find_element(By.XPATH, f"//td/span[@data-date='{today_str}']")
        driver.execute_script("arguments[0].scrollIntoView(true);", today_el)
        driver.execute_script("arguments[0].click();", today_el)
        logger.info(f"📆 Выбрана сегодняшняя дата: {today_str}")
        time.sleep(0.3)
    except Exception as e:
        logger.warning(f"Не удалось выбрать сегодняшнюю дату: {e}")
        return False

    return True

# -------------------- Основная логика --------------------
def sync_selenium_logic(raw_link: str) -> bool:
    logger.info("🚀 Запуск sync_selenium_logic()")
    link = raw_link or ""
    if "language=" in link:
        import re
        link = re.sub(r"(language=)[^&]+", r"\1EN", link)

    logger.info(f"🔍 Открываем ссылку: {link}")
    driver = _remote_driver()
    if not driver:
        logger.error("Нет доступного WebDriver-а.")
        return False

    try:
        driver.get(link)
        time.sleep(2)

        # ---------------- кнопка Edit ----------------
        try:
            edit_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//i[contains(@class,'pi-pencil')]] | //button[normalize-space(text())='Edit'] | //button[contains(., 'Rediģēt')]")
                )
            )
            edit_btn.click()
            logger.info("✏️ Нажата кнопка Edit (редактировать).")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Не удалось найти/нажать Edit: {e}", exc_info=True)
            return False

        # ---------------- выбрать дату ----------------
        if not select_today_in_calendar(driver):
            logger.warning("⚠ Не удалось выбрать сегодняшнюю дату в календаре.")
            return False

        # ---------------- CAPTCHA ----------------
        try_solve_recaptcha_checkbox(driver)

        # ---------------- поиск слотов: только +3 дня ----------------
        target_offset = 3
        found_slot = None
        max_captcha_attempts = 2
        captcha_attempt = 0

        while captcha_attempt < max_captcha_attempts:
            for day_offset in range(target_offset, target_offset + 1):
                time.sleep(1)
                try:
                    slots = driver.find_elements(
                        By.XPATH,
                        "//div[contains(@class,'wizard-select-timeslot-div') or contains(@class,'timeslot')]"
                    )
                except Exception:
                    slots = []

                for s in slots:
                    try:
                        cls = (s.get_attribute("class") or "").lower()
                        if any(x in cls for x in ("slot-full", "slot-unavailable", "slot-past")):
                            continue
                        if s.is_displayed():
                            try:
                                target = s.find_element(By.CSS_SELECTOR, ".slot-duration-span")
                            except Exception:
                                target = s

                            driver.execute_script("arguments[0].scrollIntoView(true);", s)
                            time.sleep(0.2)
                            driver.execute_script("arguments[0].click();", target)

                            found_slot = s
                            break
                    except Exception:
                        pass

                if found_slot:
                    break

            # ---------------- ПАРСИНГ РЕАЛЬНОЙ ДАТЫ ----------------
            slot_date_text = None
            if found_slot:
                try:
                    slot_date_text = (
                        found_slot.get_attribute("data-date")
                        or found_slot.get_attribute("data-datetime")
                    )
                except:
                    pass

                if not slot_date_text:
                    try:
                        slot_date_text = found_slot.text.strip()
                    except:
                        pass

            # Если капча не пройдена — пробуем ещё раз
            if slot_date_text == "Please complete CAPTCHA to view available time slots.":
                logger.warning("⚠ CAPTCHA не пройдена — пробуем ещё раз")
                try_solve_recaptcha_checkbox(driver)
                captcha_attempt += 1
                found_slot = None
                slot_date_text = None
                continue
            else:
                break

        if not found_slot:
            logger.info("⚠ Свободных слотов нет через +3 дня.")
            return False

        if not slot_date_text:
            d = datetime.now() + timedelta(days=target_offset)
            slot_date_text = d.strftime("%d.%m.%Y")

        logger.info(f"🎯 ТОЧНАЯ ДАТА СВОБОДНОГО СЛОТА: {slot_date_text}")
        logger.info("📝 РЕЖИМ ОТЛАДКИ: Save НЕ нажимаю.")

        return True

    except Exception as e:
        logger.error(f"🔥 Ошибка в sync_selenium_logic: {e}", exc_info=True)
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

# -------------------- ASYNC --------------------
async def process_booking(link: str) -> bool:
    logger.info("🚀 Запуск process_booking()")
    try:
        result = await asyncio.to_thread(sync_selenium_logic, link)
        logger.info(f"📌 Результат проверки: {result}")
        return bool(result)
    except Exception as e:
        logger.exception(f"💥 Ошибка в process_booking: {e}")
        return False

# -------------------- Тест --------------------
if __name__ == "__main__":
    test_link = "https://live.qms.goswift.eu/lvborder/booking/review/YOUR-ID/edit?language=EN"
    asyncio.run(process_booking(test_link))
