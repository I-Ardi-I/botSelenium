import logging
import os

from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")

    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=3
    )
    file_handler.suffix = "%d-%m-%Y"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, stream_handler]
    )

    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("aiohttp").setLevel(logging.INFO)

    # Настройка уровня логирования для urllib3, selenium, asyncio
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logging.info("Логирование настроено.")
