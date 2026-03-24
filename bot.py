import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- НАЛАШТУВАННЯ ---
TOKEN = "8237013345:AAFrzlZvUyhaXRRFP3FxP1xJ97dp3CuPedE" 
APP_URL = "https://fallsins.github.io/MafiaPhuket/" 
# Твоє пряме посилання, яке ти створив у BotFather
DIRECT_APP_LINK = "https://t.me/phuketmafia_bot/play"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (АНТИ-СОН) ---
async def handle(request):
    return web.Response(text="Mafia Phuket Bot is Running!")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

# --- ОБРОБКА КОМАНДИ /start_game ---
@dp.message(Command("start_game"))
async def start_game(message: types.Message):
    # Визначаємо тип чату для вибору правильної кнопки
    if message.chat.type in ["group", "supergroup"]:
        # У ГРУПІ: використовуємо Direct Link (t.me/...)
        # Це дозволяє відкрити додаток в один клік поверх чату
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 ЗАПИСАТИСЯ НА ГРУ", url=DIRECT_APP_LINK)]
        ])
    else:
        # В ОСОБИСТИХ: використовуємо стандартний WebAppInfo
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
        # Спроба відправити афішу
        await message.answer_photo(
            photo=f"{APP_URL}mafia.jpg",
            caption=caption,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        # Якщо фото недоступне — відправляємо текст
        print(f"Photo error: {e}")
        await message.answer(caption, reply_markup=markup, parse_mode="Markdown")

# --- ГОЛОВНИЙ ЗАПУСК ---
async def main():
    # Запускаємо веб-сервер, щоб Render не "сипав" помилками 
    asyncio.create_task(start_webserver())
    print("Бот Mafia Phuket успішно запущений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот вимкнений.")
