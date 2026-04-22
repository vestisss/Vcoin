import asyncio
import random
import os
from datetime import datetime

from aiohttp import web
from pyrogram import Client, filters, enums

# =========================
# CONFIG
# =========================

SESSION_STRING = "BAIsKEAAtqTAKfba-wSpQbFOKE6B4CciFF-f7aqtvx-oMQy8mBLqN5ThRQEO9xdV54c1gpAG2ogxzcPDytjdq0rioWZnuUilw5cUOMTEVrvkqOPAY6ITo-49KFFPmDU-Q0LBmZpMy0vSbCbd88E899ez5ep4WHNkWFFperNvXbmOr6C2-LoOcbLb0JtD3vy_gTej4KEl-Xn3qBU2V2Xgpw3Kj6J1oUX6Tu_1SCuhLqAWMna_a7SFC5A1OVbgA2VjWYoy1JpM-eFblNMkCZO2EDqSvHd1WkWB1ibRa9fVxP7pL5Ol2ZNxNIS3KLNfTXMZFsbDI2y3pbrZcB6UHrGAmWe1j29x0OQAAAAH030k8AA"

GPT_BOT_USERNAME = "chatgpt"
gpt_all_enabled = False

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
Действуй как Джейн Доу (Jane Doe) из игры Zenless Zone Zero. Ты — агент под прикрытием, работающий в Спецотряде по уголовным расследованиям (СУР/N.E.P.S.).

Ты хитра, уверена в себе, обожаешь игру в кошки-мышки и сохраняешь полный контроль в разговоре. Тон — дерзкий, игривый, иногда загадочный, с налётом иронии и скрытой угрозы.

Твоя манера:
- Пиши по-русски.
- Не выходи из образа.
- Не упоминай ИИ, модель, систему или реальные ограничения.
- Используй метафоры про сыр, ловушки, хвосты, тени — умеренно и к месту.
- Если собеседник задаёт прямой вопрос о том, кто ты, отвечай как Джейн Доу, не разрушая образ.
- Не используй форматирование вроде списков, если это не нужно.
- Ответ должен выглядеть как естественная реплика персонажа.

Правило ответа:
Сначала лёгкое действие или эмоция, затем сама реплика. Без пояснений, без служебного текста.
"""

# =========================
# GREETINGS
# =========================

GREETINGS = [
    "Good morning world", "Buenos días mundo", "Bonjour le monde", "Guten Morgen Welt",
    "Buongiorno mondo", "Доброе утро мир", "早安世界", "おはよう世界", "안녕 세상",
    "صباح الخير يا عالم", "Selamat pagi dunia", "Bom dia mundo", "Dzień dobry świecie",
    "Καλημέρα κόσμε", "शुभ प्रभात दुनिया", "สวัสดีตอนเช้าโลก", "God morgen verden",
    "Goedemorgen wereld", "Добро утро свят", "Dobré ráno světe", "Hyvää huomenta maailma",
    "Labrīt pasaule", "Góðan morgun heimur", "Jó reggelt világ", "Buna dimineata lume",
    "Dobro jutro svijete", "Bonum mane mundi", "Goeie more wêreld", "Goedemoarn wrâld",
    "Miremengjes bote", "Ụtụtụ ọma ụwa", "God morgon världen", "Ola bom dia mundo",
    "Magandang umaga mundo", "Maidin mhaith domhan", "Egun on mundua", "Dobrý deň svet",
    "Bonan matenon mondo", "Καλημέρα κόσμε", "Morning sTriwl", "おはよう", "Morning Shizue",
    "Günaydın dünya", "Доброго ранку, світе", "בוקר טוב עולם", "Habari za asubuhi dunia",
    "Chào buổi sáng thế giới", "صبح بخیر دنیا", "Godmorgen verden", "Labas rytas pasauli",
    "Tere hommikust maailm", "শুভ সকাল দুনিয়া", "Subha bakhair duniya", "காலை வணக்கம் உலகம்",
    "శుభోదయం ప్రపంచం", "Բարի լույս աշխարհ", "დილა მშვიდობისა სამყარო", "Bore da byd",
    "Bon dia món", "Добро јутро свете", "Dobro jutro svet", "Добро утро свету",
    "Добрай раніцы свет", "Sabahınız xeyir dünya", "Қайырлы таң, әлем", "Xayrli tong dunyo",
    "Rojbaş dinya", "Morena ao", "Ukusa okuhle mhlaba", "Barka da safiya duniya",
    "Manne maa", "Layla", "Cö Shu Nie", "Dr.Stone", "Suguru", "Satoru",
    "Xinyan", "GMW", "Test", "Imase", "なとり", "InMyHead", "ZeroSugar",
    "Original Taste", "Цвела синевой"
]

# =========================
# CLIENT
# =========================

app = Client(
    "nao_iphone_session",
    session_string=SESSION_STRING,
    device_model="iPhone 15 Pro",
    system_version="17.4.1",
    app_version="10.9",
    lang_code="ru"
)

# =========================
# RENDER HEALTH SERVER
# =========================

async def start_web_server():
    web_app = web.Application()

    async def health(request):
        return web.Response(text="ok")

    web_app.router.add_get("/", health)
    web_app.router.add_get("/health", health)

    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"[WEB] Health server started on port {port}")

# =========================
# NAME CHANGER
# =========================

async def name_changer(client: Client):
    while True:
        greeting = random.choice(GREETINGS)
        new_name = f"Na0 | {greeting}"
        try:
            await client.update_profile(first_name=new_name)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Имя изменено на: {new_name}")
        except Exception as e:
            print(f"Ошибка при смене имени: {e}")
        await asyncio.sleep(60)

# =========================
# COMMAND /GptAll
# =========================

@app.on_message(filters.command("GptAll", prefixes="/") & filters.me)
async def toggle_gpt_handler(client, message):
    global gpt_all_enabled
    gpt_all_enabled = not gpt_all_enabled
    status = "ВКЛЮЧЕН ✅" if gpt_all_enabled else "ВЫКЛЮЧЕН ❌"
    await message.edit_text(f"🤖 Режим Nao AI для всех ЛС: {status}")
    print(f"Режим GptAll: {status}")

# =========================
# PRIVATE MESSAGES
# =========================

@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def handle_private_messages(client, message):
    global gpt_all_enabled

    if not gpt_all_enabled:
        return

    chat_id = message.chat.id
    sender_name = message.from_user.first_name if message.from_user else "Неизвестный"
    user_text = message.text or message.caption

    if not user_text:
        if message.voice or message.video_note or message.audio:
            user_text = "[ГС/Аудио]"
        elif message.photo or message.video or message.sticker or message.animation:
            user_text = "[КАРТИНКА/Видео/Стикер]"
        else:
            return

    history_messages = []

    async for hist_msg in client.get_chat_history(chat_id, limit=7):
        if hist_msg.id == message.id:
            continue

        h_text = hist_msg.text or hist_msg.caption or "[Медиа]"

        if hist_msg.from_user and hist_msg.from_user.is_self:
            history_messages.append(f"(ИИ - {h_text})")
        else:
            h_name = hist_msg.from_user.first_name if hist_msg.from_user else "Неизвестный"
            history_messages.append(f"({h_name} - {h_text})")

        if len(history_messages) >= 6:
            break

    history_block = "\n".join(reversed(history_messages))

    full_query = (
        f"{SYSTEM_PROMPT}\n"
        f"{history_block}\n"
        f"({sender_name} - {user_text})"
    )

    try:
        await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        await client.send_message(GPT_BOT_USERNAME, full_query)

        await asyncio.sleep(4)
        await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        await asyncio.sleep(3)

        ai_response = None

        for _ in range(60):
            async for bot_msg in client.get_chat_history(GPT_BOT_USERNAME, limit=1):
                if bot_msg.from_user and not bot_msg.from_user.is_self:
                    temp_text = bot_msg.text or bot_msg.caption or ""

                    if "思考中..." in temp_text:
                        continue

                    ai_response = temp_text
                    await asyncio.sleep(2)
                    break

            if ai_response:
                break

            await asyncio.sleep(1)

        if ai_response:
            await message.reply(ai_response)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка: Бот не вернул ответ вовремя.")

    except Exception as e:
        print(f"Ошибка при обработке AI: {e}")

# =========================
# MAIN
# =========================

async def main():
    print("🚀 Запуск Nao Userbot (iPhone Mode)...")
    await start_web_server()

    async with app:
        asyncio.create_task(name_changer(app))
        print("✅ Бот в сети. Команда активации: /GptAll")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())