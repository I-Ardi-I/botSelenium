import config
import logging
from aiogram import types
from lang.texts import SETTINGS_RESET

logger = logging.getLogger(__name__)


async def cmd_stop(message: types.Message):
    config.ACCESS = 0
    config.MAIN_HTML = None
    config.AUTO_HTML = None
    await message.answer(SETTINGS_RESET)
    logger.info(f'Пользователь id:{message.from_user.id} сбросил настройки авторизации.')
