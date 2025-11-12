import config
import logging
from aiogram import types
from lang.texts import DENIED_ACCESS
from functions.time_checker import check_dates

logger = logging.getLogger(__name__)


async def cmd_date(message: types.Message):
    try:
        if config.ACCESS > 0:
            info = await check_dates()
            await message.answer(info)
            logger.info(f'Пользователь id:{message.from_user.id} получил информацию о датах.')
        else:
            await message.answer(DENIED_ACCESS)
            logger.error(f'Пользователь id:{message.from_user.id} пытался получить информацию о датах без доступа.')
    except Exception as ex:
        logger.error(f'Ошибка при получении свободных дат: {ex}.')
