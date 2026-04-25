from aiogram import Router, F, types
from aiogram.filters import Command
from core.engine import BotOrchestrator

def setup_router(orchestrator: BotOrchestrator):
    router = Router()

    # Обработка команды /start
    @router.message(Command("start"))
    async def cmd_start(message: types.Message):
        text = orchestrator.get_text("start")
        kb = orchestrator.get_keyboard("start")
        await message.answer(text, reply_markup=kb)

    # Универсальный обработчик всех кнопок
    @router.callback_query()
    async def universal_callback_handler(callback: types.CallbackQuery):
        # Парсим callback_data (действие:данные:следующее_меню)
        data = callback.data.split(":")
        action, payload, next_menu = data[0], data[1], data[2]

        if action == "open_menu":
            # Просто переходим к другому пункту меню из конфига
            text = orchestrator.get_text(next_menu)
            kb = orchestrator.get_keyboard(next_menu)
            await callback.message.edit_text(text, reply_markup=kb)
        
        elif action == "call_func":
            # Здесь будет вызов функций (например, статус системы)
            # Пока просто уведомление
            await callback.answer(f"Выполняю функцию: {payload}", show_alert=True)
            
        elif action == "run_script":
            # Здесь будет запуск скриптов из data/scripts
            await callback.answer(f"Запуск скрипта: {payload}", show_alert=True)

        await callback.answer()

    return router