#!/usr/bin/env python3
# bot.py
"""
Telegram бот для нумерологических расчётов
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from handlers.menu import start_command, menu_command, show_menu, info_callback
from handlers.calculations import (
    calc_phone_start, calc_phone_process,
    calc_address_start, calc_address_process,
    calc_birth_start, calc_birth_process,
    cancel,
    PHONE_INPUT, ADDRESS_INPUT, BIRTH_INPUT
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Запуск бота"""
    
    # Проверка токена
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ Ошибка: Необходимо указать токен бота в config.py!")
        logger.error("Получите токен от @BotFather в Telegram")
        return
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # === ОБРАБОТЧИКИ КОМАНД ===
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))
    
    # === CONVERSATION HANDLER ДЛЯ РАСЧЁТА ПО ТЕЛЕФОНУ ===
    phone_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(calc_phone_start, pattern="^calc_phone$")],
        states={
            PHONE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_phone_process)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(phone_conv_handler)
    
    # === CONVERSATION HANDLER ДЛЯ РАСЧЁТА ПО АДРЕСУ ===
    address_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(calc_address_start, pattern="^calc_address$")],
        states={
            ADDRESS_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_address_process)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(address_conv_handler)
    
    # === CONVERSATION HANDLER ДЛЯ РАСЧЁТА ПО ДАТЕ РОЖДЕНИЯ ===
    birth_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(calc_birth_start, pattern="^calc_birth$")],
        states={
            BIRTH_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_birth_process)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(birth_conv_handler)
    
    # === CALLBACK ОБРАБОТЧИКИ ===
    application.add_handler(CallbackQueryHandler(show_menu, pattern="^menu$"))
    application.add_handler(CallbackQueryHandler(info_callback, pattern="^info$"))
    
    # Запуск бота
    logger.info("🚀 Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
