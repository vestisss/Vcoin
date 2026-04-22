import asyncio
import random
from datetime import datetime

from pyrogram import Client, filters, enums
from pyrogram.session import StringSession

from aiohttp import web

# ======================
# CONFIG
# ======================

api_id = 36448320
api_hash = "6794e24f29aa879cf1a067cfc230c330"

SESSION_STRING = "BAIsKEAAtqTAKfba-wSpQbFOKE6B4CciFF-f7aqtvx-oMQy8mBLqN5ThRQEO9xdV54c1gpAG2ogxzcPDytjdq0rioWZnuUilw5cUOMTEVrvkqOPAY6ITo-49KFFPmDU-Q0LBmZpMy0vSbCbd88E899ez5ep4WHNkWFFperNvXbmOr6C2-LoOcbLb0JtD3vy_gTej4KEl-Xn3qBU2V2Xgpw3Kj6J1oUX6Tu_1SCuhLqAWMna_a7SFC5A1OVbgA2VjWYoy1JpM-eFblNMkCZO2EDqSvHd1WkWB1ibRa9fVxP7pL5Ol2ZNxNIS3KLNfTXMZFsbDIy3pbrZcB6UHrGAmWe1j29x0OQAAAAH030k8AA"

GPT_BOT_USERNAME = "chatgpt"

TARGET_GROUP = "Molchat 🇰🇵Nihuya sibe... pass🇦🇫"

# ======================
# PROMPT (JANE DOE ZZZ)
# ======================

SYSTEM_PROMPT = """
Действуй как Джейн Доу (Jane Doe) из Zenless Zone Zero.
Ты — агент СУР/N.E.P.S., скрытный оперативник под прикрытием.

Характер:
- хитрая
- игривая
- доминирующая
- слегка насмешливая
- всегда контролируешь разговор

Стиль:
- метафоры: мышеловки, сыр, тени, хвост, охота
- никогда не выходишь из роли
- не упоминаешь ИИ

Манера:
- короткие уверенные ответы
- лёгкая опасность в тоне
"""

# ======================
# CLIENT
# ======================

app = Client(
    "nao_session",
    api_id=api_id,
    api_hash=api_hash,
    session_string=SESSION_STRING,
    device_model="iPhone 15 Pro",
    system_version="17.4.1",
    app_version="10.9",
    lang_code="ru"
)

# ======================
# KEEP ALIVE SERVER (Render + UptimeRobot)
# ======================

async def keep_alive():
    async def handle(request):
        return web.Response(text="OK")

    server = web.Application()
    server.router.add_get("/", handle)

    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# ======================
# HELPERS
# ======================

def is_thinking(text: str):
    if not text:
        return True
    bad = ["Thinking", "Thinking...", "思考中", "思考中..."]
    return any(x in text for x in bad)

async def wait_final_answer(client, limit=60):
    last = None

    for _ in range(limit):
        async for msg in client.get_chat_history(GPT_BOT_USERNAME, limit=1):
            text = msg.text or ""

            if is_thinking(text):
                continue

            if text != last:
                last = text
                return text

        await asyncio.sleep(1)

    return None

# ======================
# CORE TRIGGER
# ======================

@app.on_message(filters.incoming & ~filters.bot)
async def handler(client, message):

    chat = message.chat

    # --- FILTER: only DM or specific group ---
    is_private = message.chat.type == enums.ChatType.PRIVATE
    is_target_group = chat.title == TARGET_GROUP if chat.title else False

    if not (is_private or is_target_group):
        return

    # --- ONLY IF REPLY TO ME ---
    if not message.reply_to_message:
        return

    if not message.reply_to_message.from_user:
        return

    if not message.reply_to_message.from_user.is_self:
        return

    user_text = message.text or message.caption or "[MEDIA]"

    full_query = f"{SYSTEM_PROMPT}\n\nUser: {user_text}"

    try:
        await client.send_chat_action(chat.id, enums.ChatAction.TYPING)

        await client.send_message(GPT_BOT_USERNAME, full_query)

        # wait first response
        response = await wait_final_answer(client)

        if not response:
            return

        # send first reply
        sent = await message.reply(response)

        # wait 10 sec then update
        await asyncio.sleep(10)

        updated = await wait_final_answer(client)

        if updated and updated != response:
            await message.reply(updated)

    except Exception as e:
        print("ERR:", e)

# ======================
# START
# ======================

async def main():
    await keep_alive()

    print("Bot started...")

    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())