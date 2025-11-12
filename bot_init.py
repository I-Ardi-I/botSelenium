import logging
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from handlers import register_commands
from aiogram.types import BotCommand, BotCommandScopeDefault

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_commands(dp)


async def start_bot():
    await bot.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Авторизация"),
            BotCommand(command="/list", description="Список всех заявок"),
            BotCommand(command="/date", description="Свободные даты"),
            BotCommand(command="/auto", description="Статус тягача"),
            BotCommand(command="/stop", description="Сброс авторизации")
        ],
        scope=BotCommandScopeDefault()
    )
    logging.info("Команды установлены. Начало старта бота...")
    await dp.start_polling(bot)
