# config.example.py
# ПРИМЕР конфигурации телеграм бота
# Скопируйте этот файл в config.py и вставьте ваш токен

import os

# ВАЖНО: Получите токен от @BotFather в Telegram
# Приоритет: Environment Variable > локальное значение (для разработки)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
