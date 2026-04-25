import yaml
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

class BotNode:
    def __init__(self, key, text, buttons):
        self.key = key
        self.text = text
        self.buttons = buttons

class BotOrchestrator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.nodes = {}
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            for key, data in config.get('nodes', {}).items():
                self.nodes[key] = BotNode(key, data['text'], data.get('buttons', []))

    def get_node(self, node_key):
        """Метод, который вызвал ошибку — теперь он здесь точно есть"""
        return self.nodes.get(node_key)

    def get_keyboard(self, node_key):
        node = self.get_node(node_key)
        if not node:
            return None
        
        builder = InlineKeyboardBuilder()
        for btn in node.buttons:
            builder.row(types.InlineKeyboardButton(
                text=btn['text'], 
                callback_data=btn['callback_data'])
            )
        return builder.as_markup()