import os
import sys
import asyncio
import logging

from aiogram import Dispatcher
from dotenv import load_dotenv

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITSchool.settings')
import django
django.setup()

from handlers import router
from support_bot.bot import bot


async def main():
    load_dotenv()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if  __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
