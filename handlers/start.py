import logging
import config
from aiogram import types
from functions.authorization import authorization
from lang.texts import INPUT_LOG_PASS, SUCCESSFUL_AUTHORIZATION, WAIT_AUTHORIZATION, ALREADY_LOGIN

logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message):
    try:
        if (config.ACCESS != 1) and (message.from_user.id == int(config.ADMIN_CHAT_ID)):
            await message.answer(WAIT_AUTHORIZATION)
            authorization(config.LOGIN, config.PASSWORD)
            config.ACCESS = 1
            await message.answer(SUCCESSFUL_AUTHORIZATION)
            logger.info(f'Пользователь id:{message.from_user.id} успешно авторизовался.')
        elif config.ACCESS == 1:
            await message.answer(ALREADY_LOGIN)
            logger.info(f'Пользователь id:{message.from_user.id} пытался повторно авторизоваться.')
        else:
            await message.answer(INPUT_LOG_PASS)
            logger.info(f'Пользователь id:{message.from_user.id} пытался авторизоваться.')
    except Exception as ex:
        logger.error(f'Ошибка при регистрации: {ex}.')
