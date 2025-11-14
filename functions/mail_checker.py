import asyncio
from imapclient import IMAPClient
import email
from bs4 import BeautifulSoup
import logging

import bot_init
from config import ADMIN_CHAT_ID, MAIL_USER, MAIL_PASSWORD

IMAP_HOST = 'imap.mail.ru'
IMAP_PORT = 993
MAILBOX = 'INBOX'
CHECK_INTERVAL = 30  # Проверка каждые 30 секунд

logger = logging.getLogger(__name__)
processed_uids = set()


def extract_last_link(msg_bytes):
    """Извлекает последнюю ссылку из HTML-письма"""
    msg = email.message_from_bytes(msg_bytes)
    html = None

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html" and not part.get("Content-Disposition"):
                html = part.get_payload(decode=True)
                break
    elif msg.get_content_type() == "text/html":
        html = msg.get_payload(decode=True)

    if html:
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all("a", href=True)
        if links:
            return links[-1]["href"]
    return None


async def send_link(link: str):
    """Отправляет ссылку в Telegram админу"""
    try:
        message_text = f"🔗 Найдена новая ссылка:\n{link}"
        await bot_init.bot.send_message(ADMIN_CHAT_ID, message_text)
        logger.info(f"📤 Отправлена ссылка администратору: {link}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки ссылки в Telegram: {e}")


async def watch_loop():
    """Основной цикл IMAP-проверки"""
    global processed_uids

    while True:
        try:
            logger.info(f"🔌 Подключаемся к IMAP ({IMAP_HOST}:{IMAP_PORT}) под пользователем {MAIL_USER}...")

            with IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True) as server:
                try:
                    server.login(MAIL_USER, MAIL_PASSWORD)
                    logger.info(f"✅ Успешный вход в IMAP под {MAIL_USER}")
                except Exception as e:
                    logger.error(f"❌ Ошибка авторизации IMAP для {MAIL_USER}: {e}")
                    await asyncio.sleep(30)
                    continue

                try:
                    server.select_folder(MAILBOX)
                    logger.info(f"📬 Выбрана папка: {MAILBOX}")
                except Exception as e:
                    logger.error(f"❌ Ошибка выбора папки IMAP: {e}")
                    await asyncio.sleep(30)
                    continue

                # Пропускаем последние письма, чтобы не обрабатывать старые
                all_uids = server.search(['ALL'])
                for uid in all_uids[-10:]:
                    processed_uids.add(uid)

                # Основной цикл проверки новых писем
                while True:
                    try:
                        new_uids = [uid for uid in server.search(['UNSEEN']) if uid not in processed_uids]

                        if new_uids:
                            logger.info(f"📨 Найдены новые письма: {new_uids}")

                            for uid in new_uids:
                                try:
                                    resp = server.fetch([uid], ['RFC822'])
                                    raw_msg = resp[uid][b'RFC822']
                                    link = extract_last_link(raw_msg)
                                    if link:
                                        await send_link(link)
                                    else:
                                        logger.debug(f"Письмо UID={uid} не содержит ссылок.")

                                    server.add_flags([uid], '\\Seen')
                                    processed_uids.add(uid)
                                    logger.info(f"✉️ Письмо UID={uid} обработано и помечено как прочитанное")

                                except Exception as e:
                                    logger.error(f"Ошибка обработки письма UID={uid}: {e}")

                        else:
                            logger.debug("📭 Новых писем нет.")

                        await asyncio.sleep(CHECK_INTERVAL)

                    except Exception as e:
                        logger.error(f"⚠️ Ошибка во внутреннем цикле проверки IMAP: {e}, переподключаемся...")
                        break  # Разрыв соединения → переподключение

        except Exception as e:
            logger.error(f"💥 Ошибка соединения с IMAP: {e}, повтор через 15 секунд...")
            await asyncio.sleep(15)
