import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")

    logger = logging.getLogger()  # корневой логгер
    logger.setLevel(logging.DEBUG)

    # Удаляем старые хендлеры, если есть
    if logger.hasHandlers():
        logger.handlers.clear()

    # Файловый хендлер
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=3, encoding="utf-8"
    )
    file_handler.suffix = "%d-%m-%Y"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(file_handler)

    # Потоковый хендлер (консоль)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(stream_handler)

    # Логирование библиотек
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("aiohttp").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logger.info("Логирование настроено.")

