import asyncio
import logging
import os
from dotenv import load_dotenv

# Импорты aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

# Твои внутренние модули
from core.engine import BotOrchestrator
from core.router import router

# Загружаем переменные окружения
load_dotenv()

async def main():
    # Настройка логирования, чтобы видеть всё в journalctl
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # --- КРИТИЧЕСКИЙ БЛОК ДЛЯ VPS (Фикс Request Timeout) ---
    # Принудительно используем IPv4, так как IPv6 на серверах часто глючит с API Telegram
    connector = aiohttp.TCPConnector(family=aiohttp.AF_INET)
    session = AiohttpSession(connector=connector)
    # -------------------------------------------------------

    # Инициализация бота и диспетчера
    bot = Bot(token=os.getenv("BOT_TOKEN"), session=session)
    dp = Dispatcher()
    
    # Подключаем роутер с логикой кнопок
    dp.include_router(router)

    logging.info("--- Бот-Оркестратор запущен с IPv4 фиксом ---")
    
    try:
        # Запуск бесконечного опроса (polling)
        # skip_updates=True поможет игнорировать старые сообщения при перезапуске
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Критическая ошибка при работе бота: {e}")
    finally:
        # Вежливо закрываем сессию при остановке
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен вручную")