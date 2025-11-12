import config
from .start import cmd_start
from .stop import cmd_stop
from .list import cmd_list
from .date import cmd_date
from .auto import cmd_auto
from .plate import cmd_plate
from .login import cmd_login
from aiogram.filters import Command


def register_commands(dp):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_stop, Command(commands=["stop"]))
    dp.message.register(cmd_list, Command(commands=["list"]))
    dp.message.register(cmd_date, Command(commands=["date"]))
    dp.message.register(cmd_auto, Command(commands=["auto"]))
    dp.message.register(cmd_plate, lambda message: config.PLATE_PATTERN.match(message.text.upper()))
    dp.message.register(cmd_login, lambda message: '-' in message.text)
