import config
import logging
from aiogram import types
from lang.texts import DENIED_ACCESS
from functions.car_information import get_all_auto_info

logger = logging.getLogger(__name__)


async def cmd_list(message: types.Message):
    try:
        if config.ACCESS > 0:
            info = get_all_auto_info(config.MAIN_HTML)
            await message.answer(info)
            logger.info(f'Пользователь id:{message.from_user.id} получил список машин.')
        else:
            await message.answer(DENIED_ACCESS)
            logger.error(f'У пользователя id:{message.from_user.id} нет доступа к списку машин.')
    except Exception as ex:
        logger.error(f'Ошибка при получении списка машин: {ex}.')
