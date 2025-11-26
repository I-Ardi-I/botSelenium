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
            BotCommand(command="/start", description="Начать работу"),
        ],
        scope=BotCommandScopeDefault()
    )
    logging.info("Команда /start установлена. Бот запускается...")
    await dp.start_polling(bot)
