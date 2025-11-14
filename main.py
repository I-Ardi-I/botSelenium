import asyncio
from bot_init import start_bot
from logging_setup import setup_logging
from functions.mail_checker import watch_loop

# Настройка логирования
setup_logging()


async def main():
    await asyncio.gather(
        start_bot(),
		watch_loop()
    )

if __name__ == '__main__':
    asyncio.run(main())
