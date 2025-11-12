import asyncio
from bot_init import start_bot
from logging_setup import setup_logging
from functions.time_checker import periodic_check_dates

# Настройка логирования
setup_logging()


async def main():
    await asyncio.gather(
        start_bot(),
        periodic_check_dates()
    )

if __name__ == '__main__':
    asyncio.run(main())
