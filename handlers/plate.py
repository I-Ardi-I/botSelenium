import config
import logging
from aiogram import types
from functions.car_information import get_auto_info
from lang.texts import DENIED_ACCESS, DATA_GET_ERROR

logger = logging.getLogger(__name__)


async def cmd_plate(message: types.Message):
    try:
        if config.AUTO_ACCESS > 0:
            info = get_auto_info(config.MAIN_HTML, message.text.upper())
            await message.answer(info)
            logger.info(f'Пользователь id:{message.from_user.id} получил информацию об авто {message.text.upper()}.')
        else:
            await message.answer(DENIED_ACCESS)
            logger.error(f'Пользователь id:{message.from_user.id} пытался запросить информацию об авто без доступа.')
    except Exception as ex:
        await message.answer(DATA_GET_ERROR)
        logger.error(f'Ошибка при получении сведений об авто: {ex}.')
