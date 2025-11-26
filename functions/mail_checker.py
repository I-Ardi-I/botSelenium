import asyncio
from imapclient import IMAPClient
import email
from bs4 import BeautifulSoup
import logging

import bot_init
from . import date_checker
from config import ADMIN_CHAT_ID, MAIL_USER, MAIL_PASSWORD

IMAP_HOST = 'imap.mail.ru'
IMAP_PORT = 993
MAILBOX = 'INBOX'
CHECK_INTERVAL = 10  # Проверка каждые 10 секунд

logger = logging.getLogger(__name__)

processed_uids = set()
processing_event = asyncio.Event()  # Ждём завершения date_checker


def extract_last_link(msg_bytes):
    """Извлекает ссылку вида .../booking/review/.../edit из письма"""

    msg = email.message_from_bytes(msg_bytes)
    html = None

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html" and not part.get("Content-Disposition"):
                html = part.get_payload(decode=True)
                break
    elif msg.get_content_type() == "text/html":
        html = msg.get_payload(decode=True)

    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    # Ищем любую ссылку на review/edit
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/booking/review/" in href and href.endswith("/edit?language=LV"):
            return href

        # если язык иной, ловим просто edit
        if "/booking/review/" in href and "/edit" in href:
            return href

    return None


async def send_link_to_tg(link: str):
    """Отправляем найденную ссылку админу через Telegram"""
    msg = f"🔗 Найдена новая ссылка:\n{link}"

    try:
        await bot_init.bot.send_message(ADMIN_CHAT_ID, msg)
        logger.info(f"📤 Ссылка отправлена в Telegram: {link}")
    except Exception as e:
        logger.error(f"Ошибка отправки Telegram: {e}")


async def handle_link(link: str):
    """Отправляем ссылку в TG и передаём в date_checker"""
    try:
        await send_link_to_tg(link)

        logger.info(f"🔄 Передаём ссылку в date_checker.process_booking: {link}")

        # ЯВНОЕ логирование перед вызовом
        logger.info("🟢 ВЫЗОВ date_checker.process_booking()")

        success = await date_checker.process_booking(link)

        logger.info(f"🔚 date_checker завершил работу. success={success}")

        if success:
            await bot_init.bot.send_message(
                ADMIN_CHAT_ID,
                "✅ Бронь успешно сделана! Возвращаюсь к парсингу писем."
            )
        else:
            await bot_init.bot.send_message(
                ADMIN_CHAT_ID,
                "⚠ date_checker завершил без успеха, будет пробовать снова."
            )

    except Exception as e:
        logger.exception(f"💥 Ошибка в handle_link: {e}")

    finally:
        processing_event.set()


async def watch_loop():
    global processed_uids, processing_event

    while True:
        try:
            logger.info(f"🔌 Подключаемся к IMAP ({IMAP_HOST}:{IMAP_PORT}) под пользователем {MAIL_USER}...")

            with IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True) as server:
                server.login(MAIL_USER, MAIL_PASSWORD)
                server.select_folder(MAILBOX)
                logger.info("✅ IMAP готов к проверке")

                while True:
                    new_uids = [
                        uid for uid in server.search(['UNSEEN', 'FROM', 'ardi.07@mail.ru'])
                        if uid not in processed_uids
                    ]

                    if new_uids:
                        uid = new_uids[0]
                        logger.info(f"📨 Найдено новое письмо UID={uid}")

                        resp = server.fetch([uid], ['RFC822'])
                        raw_msg = resp[uid][b'RFC822']
                        link = extract_last_link(raw_msg)

                        logger.info(f"🔗 Извлечённая ссылка: {link}")

                        if link:
                            processing_event.clear()
                            await handle_link(link)
                            await processing_event.wait()
                        else:
                            logger.warning("⚠ В письме НЕ НАЙДЕНА ссылка!")

                        server.add_flags([uid], '\\Seen')
                        processed_uids.add(uid)
                        logger.info(f"✉️ Письмо UID={uid} обработано")

                    else:
                        logger.debug("📭 Новых писем нет. Ждём...")

                    await asyncio.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.exception(f"💥 Ошибка IMAP, пробую снова через 15 секунд")
            await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(watch_loop())
