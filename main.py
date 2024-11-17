# bot/main.py
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import asyncio
import sqlite3
# Хендлер старту
from aiogram.filters import Command

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

# Оновлена глобальна клавіатура
def global_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Реєстрація"))
    kb.add(KeyboardButton(text="Довідка"))
    kb.add(KeyboardButton(text="Цікава кнопка"))
    return kb.as_markup(resize_keyboard=True)

# Клавіатура для опцій реєстрації
def registration_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Реєстрація делегатів від ОСС"))
    kb.add(KeyboardButton(text="Надіслати підписаний мандат"))
    kb.add(KeyboardButton(text="Реєстрація студентів-відвідувачів НСФ"))
    kb.add(KeyboardButton(text="Реєстрація організацій на алею ГО"))
    return kb.as_markup(resize_keyboard=True)
# Клавіатура для "Довідка"
def help_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Інформація про УАС"))
    kb.add(KeyboardButton(text="Долучитись до команди УАС"))
    kb.add(KeyboardButton(text="Довідка про ХХ ГА"))
    kb.add(KeyboardButton(text="Зв‘язок"))
    return kb.as_markup(resize_keyboard=True)
# Клавіатура для "Цікава кнопка"
def interesting_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Цікава кнопка"))
    kb.add(KeyboardButton(text="Реєстрація для Святого Миколая"))
    return kb.as_markup(resize_keyboard=True)

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()  # Очищаємо стан
    await message.answer(
        "На зв’язку Українська асоціація студентів! 👋🏻\n"
        "І ми запрошуємо тебе відсвяткувати наш 25-й день народження на ХХ ювілейній Генеральній асамблеї УАС! 🎉 \n"
        "Генеральна асамблея — це найвищий керівний орган Асоціації, де ми разом з тобою ухвалюватимемо важливі рішення, будуватимемо плани на майбутнє та спільно об’єднаємо зусилля заради розвитку консолідованої студентської спільноти України.\n"
        "📅 Коли? 06-08 грудня 2024 року\n"
        "📍 Де? місто Київ \n\n"
        "🎓 Окрім Генеральної асамблеї, ми підготували для тебе ще одну важливу подію — Національний студентський форум!\n"
        "Форум стане унікальною платформою для обговорення актуальних питань студентства, обміну досвідом та формування спільних ініціатив. Разом ми знайдемо нові шляхи для розвитку студентського самоврядування та підсилення голосу кожного студента! 🌟\n"
        "Стань частинкою змін, що формують майбутнє студентства, та долучися до обговорень, які створюють нові можливості для молоді України! 🚀",
        reply_markup=global_keyboard()  # Виводимо оновлену глобальну клавіатуру
    )


# Хендлер для кнопки "Реєстрація"
@dp.message(lambda message: message.text == "Реєстрація")
async def registration_options(message: types.Message):
    await message.answer(
        "Оберіть тип реєстрації:",
        reply_markup=registration_keyboard()
    )
# Хендлер для кнопки "Довідка"
@dp.message(lambda message: message.text == "Довідка")
async def help_menu(message: types.Message):
    await message.answer(
        "Оберіть, що вас цікавить:",
        reply_markup=help_keyboard()
    )
# Хендлер для кнопки "Цікава кнопка"
@dp.message(lambda message: message.text == "Цікава кнопка")
async def interesting_menu(message: types.Message):
    await message.answer(
        "Оберіть дію:",
        reply_markup=interesting_keyboard()
    )
# Хендлер для кнопки "Інформація про УАС"
@dp.message(lambda message: message.text == "Інформація про УАС")
async def info_about_uas(message: types.Message):
    await message.answer(
        "😍 Важливі факти про УАС, які варто знати кожному!\n"
        "ХТО МИ?\n"
        "Українська асоціація студентів (УАС) є однією з найбільших молодіжних організацій в Україні. 🏖 Наша діяльність спрямована на розвиток потенціалу студентської молоді та захист прав кожного студента. Асоціація є єдиною українською студентською організацією, що визнана як національне об'єднання студентів України на міжнародній арені.\n"
        "НАША КОДОВА ФРАЗА?Думка студентів має силу!\n"
        "Будемо перевіряти кодову фразу на Генеральній асамблеї, готуйся 😉\n"
        "ХТО ВХОДИТЬ ДО УАС? 🤝\n"
        "УАС об'єднує більше 160 закладів вищої та фахової передвищої освіти з майже мільйоном студентів та активно співпрацює з понад 40 студентськими союзами європейських країн. Це дозволяє асоціації бути представником інтересів українського студентства в Європейському союзі студентів (ESU).\n"
        "НАША МЕТА\n"
        "УАС - це не просто організація, вона є втіленням сміливої візії - від активного студента - до свідомого громадянина. У нашому баченні, ми прагнемо до створення освітнього середовища, де студенти є свідомими, високоосвіченими та мають силу своєї думки.💛\n"
        "МИ ЗАВЖДИ РАДІ ДОПОМОГТИ 🥰 \n"
        "Наша перша і найважливіша цінність - це відкритість. УАС відкрита до всіх студентів, які відчувають, що їхні права порушені або прагнуть, щоб їхні інтереси були належним чином представлені та захищені. Кожен студент має право безпосередньо звернутися до будь-якого органу або посадової особи УАС з метою отримання допомоги та підтримки.\n"
        "СТУДЕНТИ МАЮТЬ БУТИ ПОЧУТИМИ ☝️ \n"
        "УАС є організацією, підконтрольною лише студентам. Ми не підлягаємо жодному зовнішньому впливу або контролю. Наші завдання та мета формуються виключно відповідно до потреб і бажань студентства. Тому ми можемо ефективно захищати інтереси студентів, незалежно від того, хто може бути втягнутий у конфлікт.\n"
        "І ЯК ГЕРОДОТ ЛЮБИВ 🤌\n"
        "Внутрішня демократія є основою нашої діяльності, яка базується на системі “стримувань і противаг” та діючій системі внутрішніх регламентних норм, за якою ніхто не має ні монополії на істину, ні можливості “творити, що заманеться” без огляду на інтереси інших.\n"
        "Приєднуйтесь до команди УАС і разом ми зможемо покращити студентське життя!🔔")

# Хендлер для кнопки "Долучитись до команди УАС"
@dp.message(lambda message: message.text == "Долучитись до команди УАС")
async def join_uas_team(message: types.Message):
    await message.answer(
        "Долучитись до команди УАС \n"
        "Дякуємо за твоє бажання стати частинкою великої родини УАС-Team! Хутчіш заповнюй форму та доєднуйся до команди!\n"
        "https://forms.gle/2f2f6NWnH22C4ysp6 "
    )

# Хендлер для кнопки "Довідка про ХХ ГА"
@dp.message(lambda message: message.text == "Довідка про ХХ ГА")
async def info_about_ga(message: types.Message):
    await message.answer(
        "ХХ Генеральна Асамблея Української асоціації студентів відбудеться 25 грудня 2024 року. "
        "Деталі шукайте на офіційному сайті або запитайте нас через Зв‘язок."
    )

# Хендлер для кнопки "Зв‘язок"
@dp.message(lambda message: message.text == "Зв‘язок")
async def contact_info(message: types.Message):
    await message.answer(
        "Для зв'язку з нами використовуйте наступні канали:\n"
        "📧 Email: support@uas.org.ua\n"
        "📞 Телефон: +38 (067) 123-45-67\n"
        "🌐 Сайт: https://uas.org.ua/"
    )

# Хендлер для кнопки "Цікава кнопка"
@dp.message(lambda message: message.text == "Цікава кнопка")
async def interesting_button(message: types.Message):
    await message.answer(
        "Цікава кнопка - це просто цікава кнопка! Більше функціоналу буде додано пізніше. :)"
    )

# Хендлер для кнопки "Реєстрація для Святого Миколая"
@dp.message(lambda message: message.text == "Реєстрація для Святого Миколая")
async def register_for_st_nicholas(message: types.Message):
    await message.answer(
        "Щоб зареєструватися для участі у програмі Святого Миколая, заповніть форму на сайті:\n"
        "https://mikola.org.ua/\n\n"
        "Якщо у вас є питання, звертайтеся за email: mikola@uas.org.ua"
    )

# Хендлер для кнопки "Реєстрація делегатів від ОСС"
@dp.message(lambda message: message.text == "Реєстрація делегатів від ОСС")
async def register_delegates(message: types.Message, state: FSMContext):
    await state.clear()  # Очищуємо стан перед початком реєстрації
    await message.answer(
        "Привіт! Нам 25 років, і ми проводимо осамблею. \nВиберіть ваш ОСС із переліку:"
    )
    await show_oss_keyboard(message)  # Виклик функції для показу університетів

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

                                                    #ЗВІДСИ МОЖЕШЬ ВЗЯТИ ДАННІ ДЛЯ ЕКСЕЛЬ

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
