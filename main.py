import asyncio
import logging
import os
import socket
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

from core.engine import BotOrchestrator
from core.router import router

load_dotenv()

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # IPv4 Фикс
    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    client_session = aiohttp.ClientSession(connector=connector)
    session = AiohttpSession()
    session._session = client_session 

    bot = Bot(token=os.getenv("BOT_TOKEN"), session=session)
    dp = Dispatcher()
    
    # Инициализируем оркестратор
    orchestrator = BotOrchestrator("data/configs/default_tree.yaml")
    
    # ВАЖНО: Пробрасываем оркестратор в роутер через workflow_data
    # Теперь роутер будет видеть 'orchestrator' в аргументах функций
    dp["orchestrator"] = orchestrator
    
    dp.include_router(router)

    logging.info("--- Бот-Оркестратор запущен: IPv4 форсирован, данные связаны ---")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()
        if not client_session.closed:
            await client_session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")