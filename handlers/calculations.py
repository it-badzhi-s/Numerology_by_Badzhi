# handlers/calculations.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from data.phone_meanings import get_phone_meaning
from data.address_meanings import get_address_meaning
from data.birth_meanings import get_birth_meaning


# Состояния для ConversationHandler
PHONE_INPUT, ADDRESS_INPUT, BIRTH_INPUT = range(3)


def get_back_to_menu_keyboard():
    """Клавиатура для возврата в меню"""
    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)


# === РАСЧЁТ ПО ТЕЛЕФОНУ ===
async def calc_phone_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало расчёта по номеру телефона"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📱 Расчёт по номеру телефона\n\n"
        "Введите ваш номер телефона в любом формате:\n"
        "Например: +79991234567 или 89991234567\n\n"
        "Для отмены введите /cancel"
    )
    
    return PHONE_INPUT


async def calc_phone_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка номера телефона"""
    phone = update.message.text
    
    # Извлекаем только цифры
    digits = ''.join(filter(str.isdigit, phone))
    
    if not digits:
        await update.message.reply_text(
            "❌ Некорректный номер. Попробуйте ещё раз или /cancel для отмены."
        )
        return PHONE_INPUT
    
    # Выполняем нумерологический расчёт
    result_number = calculate_numerology_sum(digits)
    meaning = get_phone_meaning(result_number)
    
    result_text = f"""
📱 Результат расчёта по номеру телефона

Ваш номер: {phone}
Нумерологическое число: {result_number}

{meaning}
    """
    
    await update.message.reply_text(
        result_text,
        reply_markup=get_back_to_menu_keyboard()
    )
    
    return ConversationHandler.END


# === РАСЧЁТ ПО АДРЕСУ ===
async def calc_address_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало расчёта по адресу"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🏠 Расчёт по адресу\n\n"
        "Введите ваш адрес:\n"
        "Например: ул. Пушкина, д. 25, кв. 17\n\n"
        "Для отмены введите /cancel"
    )
    
    return ADDRESS_INPUT


async def calc_address_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка адреса"""
    address = update.message.text
    
    # Извлекаем цифры из адреса
    digits = ''.join(filter(str.isdigit, address))
    
    if not digits:
        await update.message.reply_text(
            "❌ В адресе должны быть числа (номер дома, квартиры). Попробуйте ещё раз или /cancel для отмены."
        )
        return ADDRESS_INPUT
    
    result_number = calculate_numerology_sum(digits)
    meaning = get_address_meaning(result_number)
    
    result_text = f"""
🏠 Результат расчёта по адресу

Ваш адрес: {address}
Нумерологическое число: {result_number}

{meaning}
    """
    
    await update.message.reply_text(
        result_text,
        reply_markup=get_back_to_menu_keyboard()
    )
    
    return ConversationHandler.END


# === РАСЧЁТ ПО ДАТЕ РОЖДЕНИЯ ===
async def calc_birth_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало расчёта по дате рождения"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🎂 Расчёт по дате рождения\n\n"
        "Введите вашу дату рождения:\n"
        "Формат: ДД.ММ.ГГГГ (например, 15.03.1990)\n\n"
        "Для отмены введите /cancel"
    )
    
    return BIRTH_INPUT


async def calc_birth_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка даты рождения"""
    birth_date = update.message.text
    
    # Извлекаем цифры
    digits = ''.join(filter(str.isdigit, birth_date))
    
    if len(digits) != 8:
        await update.message.reply_text(
            "❌ Некорректная дата. Используйте формат ДД.ММ.ГГГГ\n"
            "Попробуйте ещё раз или /cancel для отмены."
        )
        return BIRTH_INPUT
    
    result_number = calculate_numerology_sum(digits)
    meaning = get_birth_meaning(result_number)
    
    result_text = f"""
🎂 Результат расчёта по дате рождения

Ваша дата: {birth_date}
Число жизненного пути: {result_number}

{meaning}
    """
    
    await update.message.reply_text(
        result_text,
        reply_markup=get_back_to_menu_keyboard()
    )
    
    return ConversationHandler.END


# === ОТМЕНА ОПЕРАЦИИ ===
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущей операции"""
    from handlers.menu import get_main_menu_keyboard, MENU_TEXT
    
    await update.message.reply_text(
        "Операция отменена.\n\n" + MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )
    
    return ConversationHandler.END


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def calculate_numerology_sum(digits: str) -> int:
    """
    Вычисляет нумерологическую сумму (сводит к числу от 1 до 9 или мастер-числам 11, 22, 33)
    """
    total = sum(int(d) for d in digits)
    
    # Сводим к однозначному числу, но сохраняем мастер-числа
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    
    return total
