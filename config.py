# config.py
# Конфигурация телеграм бота

import os

# ВАЖНО: Получите токен от @BotFather в Telegram
# Приоритет: Environment Variable > config.local.py (для разработки)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT_TOKEN_LOCAL")

if not BOT_TOKEN:
    # Попытка загрузить из локального файла (только для разработки)
    try:
        from config.local import BOT_TOKEN as LOCAL_TOKEN
        BOT_TOKEN = LOCAL_TOKEN
    except ImportError:
        pass

# Канал для обязательной подписки
# Для публичного канала: "@channelname"
# Для приватного канала: "-1001234567890" (Chat ID)
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "-1003648407179")

# Пригласительная ссылка на канал (для приватных каналов)
CHANNEL_INVITE_LINK = os.getenv("CHANNEL_INVITE_LINK", "https://t.me/+1OtCMx8zhaY0NzVi")

# Текстовые константы
WELCOME_MESSAGE = """
🔮 Добро пожаловать в Нумерологический Бот!

Я помогу вам узнать тайны чисел и их влияние на вашу жизнь.
Выберите интересующий вас расчёт из меню ниже.
"""

MENU_TEXT = """
📋 Главное меню:

Выберите тип расчёта:
"""
