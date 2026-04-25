import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from core.engine import BotOrchestrator

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, orchestrator: BotOrchestrator):
    logging.info(f"DEBUG: Получена команда /start от пользователя {message.from_user.id}")
    
    # Получаем стартовую ноду из конфига
    node = orchestrator.get_node("start")
    
    if node:
        # Генерируем клавиатуру
        kb = orchestrator.get_keyboard("start")
        await message.answer(node.text, reply_markup=kb)
        logging.info("DEBUG: Ответ отправлен успешно")
    else:
        logging.error("DEBUG: Нода 'start' не найдена в конфиге!")
        await message.answer("Ошибка: Начальное меню не настроено.")

# Хендлер-ловушка для ЛЮБЫХ других сообщений (чтобы понять, почему не работает)
@router.message()
async def any_message(message: types.Message):
    logging.info(f"DEBUG: Поймано необработанное сообщение: {message.text} от ID {message.from_user.id}")