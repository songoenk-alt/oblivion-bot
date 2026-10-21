# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, admin
from middlewares.subscription import SubscriptionMiddleware
from database import init_db

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Инициализация SQLite базы данных
    init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключение Middleware
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    
    # Регистрация роутеров
    dp.include_router(admin.router)
    dp.include_router(start.router)
    
    print("Бот успешно запущен с базой данных...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())