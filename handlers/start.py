import logging
from aiogram import types

logger = logging.getLogger(__name__)

async def cmd_start(message: types.Message):
    try:
        await message.answer("👋 Привет! Бот работает.")
        logger.info(f"Пользователь {message.from_user.id} получил приветственное сообщение.")
    except Exception as ex:
        logger.error(f"Ошибка в cmd_start: {ex}")
