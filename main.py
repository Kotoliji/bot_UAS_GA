# bot/main.py
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import asyncio
import sqlite3


# Підключення до бази даних
DB_FILE = "registration.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Ініціалізація бота
BOT_TOKEN = "8075180480:AAEngdrSgnU0N50pb8cJSN5Y2eZMGf0Kf60"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM для збору даних
class RegistrationForm(StatesGroup):
    select_oss = State()
    select_delegate = State()
    full_name = State()
    dates = State()
    travel = State()
    daily_limit = State()
    food_preferences = State()
    medical_info = State()
    suggestions = State()
    confirmation = State()

# Створення таблиці для зберігання даних
def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delegates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT,
        oss TEXT,
        delegate_type TEXT,
        full_name TEXT,
        dates TEXT,
        travel TEXT,
        daily_limit REAL,
        food_preferences TEXT,
        medical_info TEXT,
        suggestions TEXT
    )
    """)
    conn.commit()

init_db()

# Глобальна клавіатура
def global_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Довідка"))
    kb.add(KeyboardButton(text="Інформація про УАС"))
    kb.add(KeyboardButton(text="Долучитись до команди УАС"))
    return kb.as_markup(resize_keyboard=True)

# Хендлер старту
from aiogram.filters import Command

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привіт! Нам 25 років, і ми проводимо осамблею. \nВиберіть ваш ОСС із переліку:",
        reply_markup=global_keyboard()
    )
    await show_oss_keyboard(message)

# Хендлер для обробки кнопки "Інформація про УАС"
@dp.message(lambda message: message.text == "Інформація про УАС")
async def info_about_uas(message: types.Message):
    await message.answer(
        "Українська асоціація студентів — це об'єднання студентів для розвитку, захисту прав та підтримки молоді України. "
        "Дізнатись більше можна на нашому сайті: https://uas.org.ua/"
    )

# Хендлер для обробки кнопки "Долучитись до команди УАС"
@dp.message(lambda message: message.text == "Долучитись до команди УАС")
async def join_uas_team(message: types.Message):
    await message.answer(
        "Щоб долучитись до нашої команди, заповніть форму на сайті або напишіть нам на електронну пошту: team@uas.org.ua"
    )

# Вибір ОСС
async def show_oss_keyboard(message: types.Message):
    kb = InlineKeyboardBuilder()
    universities = ["КНУ", "КПІ", "ЧНУ", "ХНУ"]
    for uni in universities:
        kb.add(InlineKeyboardButton(text=uni, callback_data=f"oss_{uni}"))
    kb.add(InlineKeyboardButton(text="Мого ОСС нема в списку", callback_data="oss_none"))
    await message.answer("Оберіть ваш університет:", reply_markup=kb.as_markup())

@dp.callback_query(lambda c: c.data.startswith("oss_"))
async def oss_selected(callback: types.CallbackQuery, state: FSMContext):
    selected = callback.data.split("_")[1]
    if selected == "none":
        await callback.message.answer("Перейдіть до розділу 'Довідка'.")
    else:
        await state.update_data(oss=selected)
        await callback.message.answer(
            "Хто може бути делегатом?",
            reply_markup=delegate_keyboard()
        )
        await state.set_state(RegistrationForm.select_delegate)

# Клавіатура для вибору делегата
def delegate_keyboard():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="Я голова і я буду", callback_data="delegate_self")
    )
    kb.add(
        InlineKeyboardButton(text="Я голова - але буде інший", callback_data="delegate_other")
    )
    kb.add(
        InlineKeyboardButton(text="Я представник і маю мандат", callback_data="delegate_representative")
    )
    return kb.as_markup()


@dp.callback_query(lambda c: c.data.startswith("delegate_"))
async def delegate_selected(callback: types.CallbackQuery, state: FSMContext):
    delegate_types = {
        "self": "Я голова і я буду",
        "other": "Я голова - але буде інший",
        "representative": "Я представник і маю мандат"
    }
    selected_key = callback.data.split("_")[1]
    selected = delegate_types.get(selected_key, "Невідомий тип делегата")

    # Зберігаємо зрозуміле значення у стан
    await state.update_data(delegate_type=selected)
    await callback.message.answer("Введіть ваше ПІБ:")
    await state.set_state(RegistrationForm.full_name)


@dp.message(RegistrationForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("У які дні будете?")
    await state.set_state(RegistrationForm.dates)

@dp.message(RegistrationForm.dates)
async def process_dates(message: types.Message, state: FSMContext):
    await state.update_data(dates=message.text)
    await message.answer("Чи буде відрядження?")
    await state.set_state(RegistrationForm.travel)

@dp.message(RegistrationForm.travel)
async def process_travel(message: types.Message, state: FSMContext):
    await state.update_data(travel=message.text)
    await message.answer("Ліміт покриття життя на день (у грн):")
    await state.set_state(RegistrationForm.daily_limit)

@dp.message(RegistrationForm.daily_limit)
async def process_daily_limit(message: types.Message, state: FSMContext):
    try:
        # Спроба конвертувати введене значення у float
        daily_limit = float(message.text)
        if daily_limit <= 0:
            raise ValueError("Ліміт повинен бути більшим за 0.")
    except ValueError:
        # Якщо введене значення некоректне
        await message.answer("Будь ласка, введіть коректне число для ліміту покриття на день.")
        return

    # Якщо значення коректне, зберігаємо його
    await state.update_data(daily_limit=daily_limit)
    await message.answer("Харчування (особливості):")
    await state.set_state(RegistrationForm.food_preferences)

@dp.message(RegistrationForm.food_preferences)
async def process_food(message: types.Message, state: FSMContext):
    await state.update_data(food_preferences=message.text)
    await message.answer("Медичні потреби:")
    await state.set_state(RegistrationForm.medical_info)

@dp.message(RegistrationForm.medical_info)
async def process_medical_info(message: types.Message, state: FSMContext):
    await state.update_data(medical_info=message.text)
    await message.answer("Пропозиції:")
    await state.set_state(RegistrationForm.suggestions)

@dp.message(RegistrationForm.suggestions)
async def process_suggestions(message: types.Message, state: FSMContext):
    await state.update_data(suggestions=message.text)
    user_data = await state.get_data()

    # Формуємо текст для попереднього перегляду даних
    preview_text = (
        "Будь ласка, перегляньте ваші дані перед збереженням:\n"
        f"🔹 Університет: {user_data.get('oss', 'Не вказано')}\n"
        f"🔹 Тип делегата: {user_data.get('delegate_type', 'Не вказано')}\n"
        f"🔹 ПІБ: {user_data.get('full_name', 'Не вказано')}\n"
        f"🔹 Дати участі: {user_data.get('dates', 'Не вказано')}\n"
        f"🔹 Відрядження: {user_data.get('travel', 'Не вказано')}\n"
        f"🔹 Ліміт на день: {user_data.get('daily_limit', 'Не вказано')}\n"
        f"🔹 Харчові особливості: {user_data.get('food_preferences', 'Не вказано')}\n"
        f"🔹 Медичні потреби: {user_data.get('medical_info', 'Не вказано')}\n"
        f"🔹 Пропозиції: {user_data.get('suggestions', 'Не вказано')}\n\n"
        "Підтверджуєте ці дані?"
    )

    # Відправка повідомлення з попереднім переглядом та кнопками підтвердження
    await message.answer(
        preview_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Так, зберегти", callback_data="confirm_yes")],
            [InlineKeyboardButton(text="Ні, редагувати", callback_data="confirm_edit")]
        ])
    )
    await state.set_state(RegistrationForm.confirmation)


@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirmation_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "confirm_yes":
        user_data = await state.get_data()
        cursor.execute('''INSERT INTO delegates (user_id, username, oss, delegate_type, full_name, dates, travel, daily_limit, food_preferences, medical_info, suggestions)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (callback.from_user.id, callback.from_user.username, user_data['oss'], user_data['delegate_type'],
                        user_data['full_name'], user_data['dates'], user_data['travel'], user_data['daily_limit'],
                        user_data['food_preferences'], user_data['medical_info'], user_data['suggestions']))
        conn.commit()
        await callback.message.answer("Реєстрація підтверджена. Дякую!")
        await state.clear()
    elif callback.data == "confirm_edit":
        await callback.message.answer("Повертаю до редагування...")
        await state.set_state(RegistrationForm.full_name)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
