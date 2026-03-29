# handlers/menu.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from config import WELCOME_MESSAGE, MENU_TEXT, REQUIRED_CHANNEL, CHANNEL_INVITE_LINK


def get_main_menu_keyboard():
    """Создаёт клавиатуру главного меню"""
    keyboard = [
        [InlineKeyboardButton("📱 Расчёт по номеру телефона", callback_data="calc_phone")],
        [InlineKeyboardButton("🏠 Расчёт по адресу", callback_data="calc_address")],
        [InlineKeyboardButton("🎂 Расчёт по дате рождения", callback_data="calc_birth")],
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_subscription_keyboard():
    """Создаёт клавиатуру с кнопкой подписки"""
    # Если это публичный канал (начинается с @)
    if str(REQUIRED_CHANNEL).startswith("@"):
        channel_url = f"https://t.me/{REQUIRED_CHANNEL.lstrip('@')}"
    else:
        # Для приватного канала используем пригласительную ссылку
        channel_url = CHANNEL_INVITE_LINK

    keyboard = [
        [InlineKeyboardButton("📢 Подписаться на канал", url=channel_url)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверяет подписку пользователя на канал"""
    try:
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        # Пользователь подписан если статус: member, administrator, creator
        return chat_member.status in ["member", "administrator", "creator"]
    except BadRequest:
        # Если бот не имеет прав доступа к каналу
        return False
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id

    # Проверяем подписку на канал
    is_subscribed = await check_subscription(user_id, context)

    if not is_subscribed:
        # Если канал не настроен, пропускаем проверку
        if REQUIRED_CHANNEL == "@your_channel":
            await update.message.reply_text(
                WELCOME_MESSAGE + "\n" + MENU_TEXT,
                reply_markup=get_main_menu_keyboard()
            )
        else:
            # Показываем сообщение с требованием подписки
            subscription_message = f"""🔮 **Добро пожаловать в Нумерологический Бот!**

Я помогу вам узнать тайны чисел и их влияние на вашу жизнь.

📋 **Что я умею:**
• Расчёт по номеру телефона
• Расчёт по адресу проживания
• Расчёт по дате рождения

⚠️ **Важно!** Для работы бота необходимо подписаться на наш канал.

🔗 **Инструкция:**
1️⃣ Нажмите кнопку ниже → подпишитесь на канал
2️⃣ Вернитесь и нажмите «✅ Я подписался»
3️⃣ Готово! Меню бота откроется автоматически

"""
            await update.message.reply_text(
                subscription_message,
                reply_markup=get_subscription_keyboard(),
                parse_mode="Markdown"
            )
    else:
        # Пользователь подписан - показываем меню
        await update.message.reply_text(
            "✅ **Спасибо за подписку!**\n\n" + WELCOME_MESSAGE + "\n" + MENU_TEXT,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /menu"""
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)

    if not is_subscribed and REQUIRED_CHANNEL != "@your_channel":
        await update.message.reply_text(
            "⚠️ Для доступа к меню необходимо подписаться на канал!\n\n"
            "Нажмите кнопку ниже и следуйте инструкции.",
            reply_markup=get_subscription_keyboard()
        )
    else:
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


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback для проверки подписки после нажатия кнопки"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)

    if is_subscribed:
        success_message = """✅ **Отлично, вы подписались!**

Добро пожаловать в Нумерологический Бот!

"""
        await query.edit_message_text(
            success_message + WELCOME_MESSAGE + "\n" + MENU_TEXT,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(
            "❌ **Подписка не обнаружена!**\n\n"
            "Пожалуйста, убедитесь что вы:\n"
            "1️⃣ Нажали кнопку «📢 Подписаться на канал»\n"
            "2️⃣ Действительно подписались (кнопка «Вступить»)\n"
            "3️⃣ Вернулись и нажали «✅ Я подписался»\n\n"
            "Попробуйте ещё раз!",
            reply_markup=get_subscription_keyboard()
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
