import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from core.engine import BotOrchestrator
from core.router import setup_router

# Загружаем переменные из .env
load_dotenv()

async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Инициализация бота и диспетчера
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Инициализация нашего "движка"
    # Передаем путь к конфигу, который создали ранее
    orchestrator = BotOrchestrator("data/configs/default_tree.yaml")

    # Настраиваем роутер и передаем туда оркестратор
    router = setup_router(orchestrator)
    dp.include_router(router)

    logging.info("--- Бот-Оркестратор запущен ---")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("--- Бот остановлен ---")