# core/engine.py
import yaml
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class BotOrchestrator:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.menu_structure = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)['menu']

    def get_keyboard(self, menu_id: str):
        builder = InlineKeyboardBuilder()
        menu_data = self.menu_structure.get(menu_id, {})
        
        for btn in menu_data.get('buttons', []):
            # Формируем callback_data как "тип_действия:цель:следующее_меню"
            callback_data = f"{btn['action']}:{btn.get('payload', 'none')}:{btn.get('next_menu', 'none')}"
            builder.row(InlineKeyboardButton(
                text=btn['label'], 
                callback_data=callback_data
            ))
        return builder.as_markup()

    def get_text(self, menu_id: str):
        return self.menu_structure.get(menu_id, {}).get('text', "Ошибка: Меню не найдено")