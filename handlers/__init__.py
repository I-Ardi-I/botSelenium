from .start import cmd_start
from aiogram.filters import Command

def register_commands(dp):
    dp.message.register(cmd_start, Command(commands=["start"]))
