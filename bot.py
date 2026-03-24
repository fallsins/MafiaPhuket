import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- НАЛАШТУВАННЯ ---
TOKEN = "ТВІЙ_ТОКЕН" 
APP_URL = "https://fallsins.github.io/MafiaPhuket/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Код для "анти-сну" (простий веб-сервер)
async def handle(request):
    return web.Response(text="Бот працює!")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

@dp.message(Command("start_game"))
async def start_game(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 ЗАПИСАТИСЯ НА ГРУ", web_app=WebAppInfo(url=APP_URL))]
    ])
    caption = (
        "🎭 **MAFIA PHUKET | АНОНС ГРИ**\n\n"
        "Запрошуємо на вечір інтелектуально-психологічної гри.\n\n"
        "📅 **Коли:** Субота, 19:30\n"
        "📍 **Де:** Ali BBQ Kathu\n"
        "💵 **Внесок:** 100 THB\n\n"
        "Для реєстрації тисніть кнопку нижче 👇"
    )
    try:
        await message.answer_photo(photo=f"{APP_URL}mafia.jpg", caption=caption, reply_markup=markup, parse_mode="Markdown")
    except:
        await message.answer(caption, reply_markup=markup, parse_mode="Markdown")

async def main():
    # Запускаємо веб-сервер паралельно з ботом
    asyncio.create_task(start_webserver())
    print("Бот Mafia Phuket запущений на Render...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
