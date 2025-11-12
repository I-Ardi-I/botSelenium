import config
import logging
from aiogram import types
from functions.authorization import authorization
from lang.texts import SUCCESSFUL_AUTHORIZATION, ERROR_LOG_PASS, INCORRECT_LOG_PASS, ALREADY_LOGIN

logger = logging.getLogger(__name__)


async def cmd_login(message: types.Message):
    try:
        config.LOG, config.PASS = message.text.split(' - ')
        if config.ACCESS != 1 and authorization(config.LOG, config.PASS):
            config.ACCESS = 1
            await message.answer(SUCCESSFUL_AUTHORIZATION)
            logger.info(f'Пароль пользователя id:{message.from_user.id} принят.')
        elif config.ACCESS == 1:
            await message.answer(ALREADY_LOGIN)
        else:
            config.ACCESS = 0
            await message.answer(ERROR_LOG_PASS)
            logger.error(f'Пароль пользователя id:{message.from_user.id} отклонён.')
    except ValueError:
        await message.answer(INCORRECT_LOG_PASS)
        logger.error(f'Пользователь id:{message.from_user.id} ввёл некорректный пароль.')
