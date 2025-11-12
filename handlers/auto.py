import config
import logging
from aiogram import types
from lang.texts import CHECK_AUTO_PLATE, DENIED_ACCESS

logger = logging.getLogger(__name__)


async def cmd_auto(message: types.Message):
    try:
        if config.ACCESS > 0:
            config.AUTO_ACCESS = 1
            await message.answer(CHECK_AUTO_PLATE)
            logger.info(f'Пользователю id:{message.from_user.id} одобрен запрос на получение сведений об авто.')
        else:
            config.AUTO_ACCESS = 0
            await message.answer(DENIED_ACCESS)
            logger.info(f'Пользователь id:{message.from_user.id} пытался запросить сведения об авто без прав доступа.')
    except Exception as ex:
        logger.error(f'Ошибка при запросе на получение сведений об авто: {ex}.')
