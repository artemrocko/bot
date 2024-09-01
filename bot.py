# 7392931002:AAEgffxxN2MptXKQ48mhQKY-HGc2SIhimes

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Вставте свій токен Telegram-бота тут
TOKEN = '7392931002:AAEgffxxN2MptXKQ48mhQKY-HGc2SIhimes'

# Створимо список для збереження телефонних номерів
phone_numbers = []

# Стартове меню з вибором мови
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["Українська", "Русский"],
        ["Polski", "English"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Виберіть мову / Выберите язык / Wybierz język / Choose language:", reply_markup=reply_markup)

async def set_language(update: Update, context: CallbackContext) -> None:
    language = update.message.text
    context.user_data['language'] = language

    if language == "Українська":
        await update.message.reply_text("Доброго дня, я Ваш бот-консультант з легалізації.", reply_markup=main_menu("Українська"))
    elif language == "Русский":
        await update.message.reply_text("Здравствуйте, я ваш бот-консультант по легализации.", reply_markup=main_menu("Русский"))
    elif language == "Polski":
        await update.message.reply_text("Dzień dobry, jestem twoim botem doradcą ds. legalizacji.", reply_markup=main_menu("Polski"))
    elif language == "English":
        await update.message.reply_text("Hello, I am your legalization consultant bot.", reply_markup=main_menu("English"))
    else:
        await update.message.reply_text("Будь ласка, оберіть одну з запропонованих мов.")

def main_menu(language):
    if language == "Українська":
        keyboard = [
            ["Перелік наших послуг", "Консультація"],
            ["Контакти", "Змінити мову"]
        ]
    elif language == "Русский":
        keyboard = [
            ["Перечень наших услуг", "Консультация"],
            ["Контакты", "Изменить язык"]
        ]
    elif language == "Polski":
        keyboard = [
            ["Lista naszych usług", "Konsultacja"],
            ["Kontakt", "Zmień język"]
        ]
    else:  # English
        keyboard = [
            ["Our Services", "Consultation"],
            ["Contacts", "Change Language"]
        ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def handle_menu(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    language = context.user_data.get('language', "Українська")
    
    if text in ["Перелік наших послуг", "Перечень наших услуг", "Lista naszych usług", "Our Services"]:
        services = "\n".join([
            "1. Побит часовий / Временный вид на жительство",
            "2. Побит сталий / Постоянный вид на жительство",
            "3. Побит резидента / Вид на жительство резидента",
            "4. Подача на громадянство / Подача на гражданство",
            "5. Заміна прав / Замена водительских прав",
            "6. Заповнення анкет / Заполнение анкет",
            "7. PESEL"
        ])
        await update.message.reply_text(f"{services}\n\nДля вибраної послуги зв'яжіться за номером +48573996984.")
    
    elif text in ["Консультація", "Консультация", "Konsultacja", "Consultation"]:
        if language == "Українська":
            await update.message.reply_text("Залиште свій номер телефону, і ми з вами зв'яжемося.")
        elif language == "Русский":
            await update.message.reply_text("Оставьте свой номер телефона, и мы с вами свяжемся.")
        elif language == "Polski":
            await update.message.reply_text("Zostaw swój numer telefonu, a my się z tobą skontaktujemy.")
        elif language == "English":
            await update.message.reply_text("Leave your phone number, and we will contact you.")
    
    elif text in ["Контакти", "Контакты", "Kontakt", "Contacts"]:
        await update.message.reply_text("Телефон: +48573996984\nEmail: your_email@example.com\nInstagram: your_instagram\nFacebook: your_facebook")
    
    elif text in ["Змінити мову", "Изменить язык", "Zmień język", "Change Language"]:
        await start(update, context)

async def save_phone_number(update: Update, context: CallbackContext) -> None:
    phone_number = update.message.text

    # Перевірка, чи повідомлення виглядає як номер телефону
    if phone_number and phone_number.startswith("+") and phone_number[1:].isdigit():
        phone_numbers.append(phone_number)

        # Виводимо номер в консоль
        print(f"Новий номер телефону: {phone_number}")

        # Зберігаємо номер у файл
        with open("phone_numbers.txt", "a") as file:
            file.write(phone_number + "\n")
        
        await update.message.reply_text("Дякуємо! Ваш номер збережено, ми з вами зв'яжемося найближчим часом.")
    else:
        await update.message.reply_text("Будь ласка, введіть номер телефону у форматі +XXXXXXXXXXX.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^(Українська|Русский|Polski|English)$"), set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.Regex(r"^\+?\d{10,15}$"), save_phone_number))

    # Запускаємо бота
    application.run_polling()

if __name__ == '__main__':
    main()
