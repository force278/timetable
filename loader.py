from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.database import Database, CountRequests


DB = Database()
CR = CountRequests()

bot = Bot(token='1973883258:AAFfv4jgjr2_e1frEobYi8UJEc3PbThqLSw', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
