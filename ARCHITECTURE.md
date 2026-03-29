# 🏗️ Архитектура Нумерологического Бота

## Общая структура

```
┌─────────────────────────────────────────────────┐
│              TELEGRAM BOT API                    │
│         (python-telegram-bot library)            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              bot.py (Главный файл)               │
│  • Инициализация бота                            │
│  • Регистрация обработчиков                      │
│  • Управление ConversationHandler'ами            │
└─────────┬──────────────────────┬────────────────┘
          │                      │
          ▼                      ▼
┌──────────────────┐   ┌─────────────────────────┐
│  handlers/       │   │     config.py           │
│                  │   │  • Токен бота           │
│  • menu.py       │   │  • Текстовые константы  │
│  • calculations.py│   └─────────────────────────┘
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              data/ (Источники данных)            │
│                                                  │
│  • phone_meanings.py   - Толкования для телефонов│
│  • address_meanings.py - Толкования для адресов  │
│  • birth_meanings.py   - Толкования для дат      │
└─────────────────────────────────────────────────┘
```

## Поток данных

### 1. Запуск и Приветствие

```
Пользователь → /start
      │
      ▼
bot.py: CommandHandler("start", start_command)
      │
      ▼
handlers/menu.py: start_command()
      │
      ▼
Отправка приветственного сообщения + Меню
```

### 2. Выбор типа расчёта

```
Пользователь → Нажимает кнопку "Расчёт по телефону"
      │
      ▼
bot.py: CallbackQueryHandler(pattern="^calc_phone$")
      │
      ▼
ConversationHandler начинает диалог
      │
      ▼
handlers/calculations.py: calc_phone_start()
      │
      ▼
Запрос ввода номера телефона
      │
      ▼
Пользователь → Вводит номер
      │
      ▼
handlers/calculations.py: calc_phone_process()
      │
      ├─► calculate_numerology_sum() - Вычисление числа
      │
      └─► data/phone_meanings.py: get_phone_meaning()
            │
            ▼
      Получение толкования
            │
            ▼
      Отправка результата + Кнопка "Вернуться в меню"
```

### 3. Возврат в меню

```
Пользователь → Нажимает "Вернуться в меню"
      │
      ▼
bot.py: CallbackQueryHandler(pattern="^menu$")
      │
      ▼
handlers/menu.py: show_menu()
      │
      ▼
Показ главного меню
```

## Модули и их функции

### 📄 bot.py
**Назначение:** Точка входа, инициализация и координация

**Функции:**
- `main()` - Главная функция запуска бота

**Обработчики:**
- CommandHandler для команд `/start`, `/menu`
- 3 ConversationHandler для каждого типа расчёта
- CallbackQueryHandler для кнопок меню

### 📄 config.py
**Назначение:** Конфигурация и константы

**Содержит:**
- `BOT_TOKEN` - Токен Telegram бота
- `WELCOME_MESSAGE` - Приветственное сообщение
- `MENU_TEXT` - Текст главного меню

### 📁 handlers/

#### 📄 menu.py
**Назначение:** Управление меню и навигацией

**Функции:**
- `get_main_menu_keyboard()` - Создаёт клавиатуру меню
- `start_command()` - Обработка /start
- `menu_command()` - Обработка /menu
- `show_menu()` - Показ меню (callback)
- `info_callback()` - Информация о боте

#### 📄 calculations.py
**Назначение:** Логика расчётов и обработка ввода

**Состояния ConversationHandler:**
- `PHONE_INPUT` - Ожидание ввода телефона
- `ADDRESS_INPUT` - Ожидание ввода адреса
- `BIRTH_INPUT` - Ожидание ввода даты

**Функции для телефона:**
- `calc_phone_start()` - Начало диалога
- `calc_phone_process()` - Обработка номера

**Функции для адреса:**
- `calc_address_start()` - Начало диалога
- `calc_address_process()` - Обработка адреса

**Функции для даты:**
- `calc_birth_start()` - Начало диалога
- `calc_birth_process()` - Обработка даты

**Вспомогательные:**
- `cancel()` - Отмена операции
- `calculate_numerology_sum()` - Нумерологический расчёт
- `get_back_to_menu_keyboard()` - Кнопка возврата

### 📁 data/

#### 📄 phone_meanings.py
- `PHONE_MEANINGS` - Словарь с толкованиями (1-9, 11, 22, 33)
- `get_phone_meaning()` - Получение толкования по числу

#### 📄 address_meanings.py
- `ADDRESS_MEANINGS` - Словарь с толкованиями для адресов
- `get_address_meaning()` - Получение толкования по числу

#### 📄 birth_meanings.py
- `BIRTH_MEANINGS` - Словарь с толкованиями для дат
- `get_birth_meaning()` - Получение толкования по числу

## ConversationHandler: Как это работает

ConversationHandler - это механизм для создания многошаговых диалогов.

```python
ConversationHandler(
    entry_points=[...],    # Как начать диалог
    states={...},          # Состояния и их обработчики
    fallbacks=[...]        # Как выйти из диалога
)
```

**Пример для расчёта по телефону:**

```python
phone_conv_handler = ConversationHandler(
    entry_points=[
        # Начало: нажатие кнопки "Расчёт по телефону"
        CallbackQueryHandler(calc_phone_start, pattern="^calc_phone$")
    ],
    states={
        # Состояние: ожидание ввода телефона
        PHONE_INPUT: [
            MessageHandler(filters.TEXT, calc_phone_process)
        ]
    },
    fallbacks=[
        # Выход: команда /cancel
        CommandHandler("cancel", cancel)
    ]
)
```

**Жизненный цикл:**

1. **Entry Point:** Пользователь нажимает кнопку → вызывается `calc_phone_start()`
2. **State:** Бот переходит в состояние `PHONE_INPUT`
3. **Processing:** Ждёт текстового сообщения → вызывается `calc_phone_process()`
4. **End:** Возвращает `ConversationHandler.END` → диалог завершён

## Нумерологический расчёт

### Алгоритм приведения к числу:

```python
def calculate_numerology_sum(digits: str) -> int:
    # 1. Суммируем все цифры
    total = sum(int(d) for d in digits)
    
    # 2. Приводим к однозначному числу
    # Но сохраняем мастер-числа: 11, 22, 33
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    
    return total
```

**Примеры:**

```
Телефон: +7 999 123 45 67
Цифры: 79991234567
Сумма: 7+9+9+9+1+2+3+4+5+6+7 = 62
Приведение: 6+2 = 8 ✓

Адрес: ул. Пушкина, д. 11, кв. 22
Цифры: 1122
Сумма: 1+1+2+2 = 6 ✓

Дата: 15.03.1990
Цифры: 15031990
Сумма: 1+5+0+3+1+9+9+0 = 28
Приведение: 2+8 = 10 → 1+0 = 1 ✓

Особый случай - мастер-число:
Дата: 29.11.1992
Цифры: 29111992
Сумма: 2+9+1+1+1+9+9+2 = 34
Приведение: 3+4 = 7... но если на каком-то этапе получилось 11, 22 или 33:
Например: 29 → 2+9 = 11 (оставляем!) ✓
```

## Расширение функционала

### Как добавить новый тип расчёта:

1. **Создать файл с данными:**
   ```python
   # data/name_meanings.py
   NAME_MEANINGS = {1: "...", 2: "...", ...}
   def get_name_meaning(number): ...
   ```

2. **Добавить обработчик:**
   ```python
   # handlers/calculations.py
   NAME_INPUT = 3  # Новое состояние
   
   async def calc_name_start(): ...
   async def calc_name_process(): ...
   ```

3. **Добавить кнопку в меню:**
   ```python
   # handlers/menu.py
   keyboard = [
       ...,
       [InlineKeyboardButton("👤 Расчёт по имени", callback_data="calc_name")]
   ]
   ```

4. **Зарегистрировать в bot.py:**
   ```python
   name_conv_handler = ConversationHandler(...)
   application.add_handler(name_conv_handler)
   ```

## Безопасность и best practices

✅ **Что сделано правильно:**
- Токен вынесен в отдельный файл
- Модульная структура
- Использование ConversationHandler для диалогов
- Логирование
- Обработка ошибок ввода

🔒 **Рекомендации:**
- Добавить `config.py` в `.gitignore`
- Использовать переменные окружения для продакшена
- Добавить rate limiting для защиты от спама
- Логировать действия пользователей
- Добавить аналитику использования

## Производительность

**Текущая архитектура:**
- ✅ Легковесная (нет БД)
- ✅ Быстрая (все данные в памяти)
- ⚠️ Не сохраняет историю
- ⚠️ Теряет состояние при перезапуске

**Для масштабирования:**
- Добавить Redis для хранения состояний
- Добавить PostgreSQL для истории расчётов
- Использовать async/await везде
- Добавить кэширование часто используемых данных

---

**Эта архитектура спроектирована для:**
- ✅ Лёгкости понимания
- ✅ Простоты расширения
- ✅ Модульности
- ✅ Поддерживаемости кода
