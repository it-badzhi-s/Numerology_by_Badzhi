# handlers/menu.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WELCOME_MESSAGE, MENU_TEXT


def get_main_menu_keyboard():
    """Создаёт клавиатуру главного меню"""
    keyboard = [
        [InlineKeyboardButton("📱 Расчёт по номеру телефона", callback_data="calc_phone")],
        [InlineKeyboardButton("🏠 Расчёт по адресу", callback_data="calc_address")],
        [InlineKeyboardButton("🎂 Расчёт по дате рождения", callback_data="calc_birth")],
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        WELCOME_MESSAGE + "\n" + MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /menu"""
    await update.message.reply_text(
        MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает главное меню (используется в callback)"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )


async def info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает информацию о боте"""
    query = update.callback_query
    await query.answer()
    
    info_text = """
ℹ️ О боте:

Этот бот выполняет нумерологические расчёты на основе:
• Вашего номера телефона
• Вашего адреса проживания
• Вашей даты рождения

Нумерология — древняя наука о числах и их влиянии на судьбу человека.

Для возврата в меню нажмите кнопку ниже.
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data="menu")]]
    
    await query.edit_message_text(
        info_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
