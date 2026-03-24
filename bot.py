import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- НАЛАШТУВАННЯ ---
# Встав свій токен сюди
TOKEN = "8237013345:AAFrzlZvUyhaXRRFP3FxP1xJ97dp3CuPedE" 
# Посилання на твій GitHub Pages
APP_URL = "https://fallsins.github.io/MafiaPhuket/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (АНТИ-СОН) ---
async def handle(request):
    return web.Response(text="Бот Mafia Phuket працює!")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render використовує порт 10000 за замовчуванням
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

# --- ОБРОБКА КОМАНДИ /start_game ---
@dp.message(Command("start_game"))
async def start_game(message: types.Message):
    bot_info = await bot.get_me()
    
    # Перевіряємо, де написана команда: у групі чи в лічці
    if message.chat.type in ["group", "supergroup"]:
        # У ГРУПІ: робимо посилання на бота (Deep Link)
        # Це обходить помилку BUTTON_TYPE_INVALID
        app_link = f"https://t.me/{bot_info.username}?start=webapp"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 ЗАПИСАТИСЯ НА ГРУ", url=app_link)]
        ])
    else:
        # В ОСОБИСТИХ: відкриваємо Mini App напряму
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 ЗАПИСАТИСЯ НА ГРУ", web_app=WebAppInfo(url=APP_URL))]
        ])

    caption = (
        "🎭 **MAFIA PHUKET | АНОНС ГРИ**\n\n"
        "Запрошуємо на вечір інтелектуально-психологічної гри.\n\n"
        "📅 **Коли:** Субота, 19:30\n"
        "📍 **Де:** Ali BBQ Kathu\n"
        "💵 **Внесок:** 100 THB\n\n"
        "Для реєстрації натисніть кнопку нижче 👇"
    )

    try:
        # Намагаємось відправити з картинкою
        await message.answer_photo(
            photo=f"{APP_URL}mafia.jpg",
            caption=caption,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        # Якщо картинка не вантажиться, шлемо просто текст
        print(f"Error sending photo: {e}")
        await message.answer(caption, reply_markup=markup, parse_mode="Markdown")

# --- ЗАПУСК ---
async def main():
    # Запускаємо сервер для Render паралельно
    asyncio.create_task(start_webserver())
    print("Бот Mafia Phuket успішно запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинений.")
