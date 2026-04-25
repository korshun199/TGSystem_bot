#!/bin/bash

echo "--- Инициализация структуры прямо в корне TGSystem_bot ---"

# Создаем структуру каталогов без корневой папки
mkdir -p {core,web_panel,data/configs,data/scripts,utils,logs}

# Создаем базовые файлы
touch core/{__init__.py,engine.py,router.py,state_manager.py}
touch web_panel/{__init__.py,app.py,routes.py}
touch utils/{__init__.py,helpers.py,security.py}
touch data/configs/default_tree.yaml
touch .env
touch main.py

# Наполнение .gitignore (добавляем и сам скрипт инициализации, чтобы не мусорил в репе)
cat <<EOF > .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Project specific
logs/
data/configs/local_config.yaml
init_project.sh
EOF

# Наполнение README.md
cat <<EOF > README.md
# TGSystem_bot: Universal Orchestrator
Закапсулированный движок для динамического управления Telegram-ботами.
EOF

# Наполнение .env
echo "BOT_TOKEN=your_token_here
ADMIN_ID=your_id_here
DB_URL=sqlite+aiosqlite:///./data/bot_database.db
SECRET_KEY=$(openssl rand -hex 16)" > .env

# Инициализация Git (если репозиторий уже был, он просто подхватит изменения)
if [ ! -d ".git" ]; then
    git init
    git branch -m main
fi

git add .
git commit -m "Re-init: Структура проекта в корневой директории"

echo "--- Готово! Теперь всё на своих местах ---"