import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАЛАШТУВАННЯ ---
# Встав свій токен від @BotFather
TOKEN = "8237013345:AAFrzlZvUyhaXRRFP3FxP1xJ97dp3CuPedE" 

# Посилання на твій сайт на GitHub
APP_URL = "https://fallsins.github.io/MafiaPhuket/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start_game"))
async def start_game(message: types.Message):
    # Кнопка для відкриття Mini App
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 ЗАПИСАТИСЯ НА ГРУ", 
            web_app=WebAppInfo(url=APP_URL)
        )]
    ])
    
    caption = (
        "🎭 **MAFIA PHUKET | АНОНС ГРИ**\n\n"
        "Запрошуємо на вечір інтелектуально-психологічної гри. "
        "Кількість місць обмежена (15 осіб), решта учасників потрапляють до резерву.\n\n"
        "📅 **Коли:** Субота, 19:30\n"
        "📍 **Де:** Ali BBQ Kathu\n"
        "💵 **Внесок:** 100 THB\n\n"
        "Для реєстрації натисніть кнопку нижче 👇"
    )
    
    # Бот візьме твою картинку mafia.jpg з GitHub для анонсу
    try:
        await message.answer_photo(
            photo=f"{APP_URL}mafia.jpg",
            caption=caption,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        # Якщо картинка не завантажиться, відправить просто текст
        await message.answer(caption, reply_markup=markup, parse_mode="Markdown")

async def main():
    print("Бот Mafia Phuket запущений і готовий до роботи...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())