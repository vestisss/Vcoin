import asyncio
import logging
from aiohttp import web
from pyrogram import Client, filters, enums
from pyrogram.handlers import MessageHandler

# =========================
# CONFIG
# =========================

api_id = 36448320
api_hash = "6794e24f29aa879cf1a067cfc230c330"

# ВСТАВЬ СЮДА СВОЮ STRING SESSION / ИЛИ ОСТАВЬ ТЕКУЩУЮ
SESSION_NAME = "BAIsKEAAtqTAKfba-wSpQbFOKE6B4CciFF-f7aqtvx-oMQy8mBLqN5ThRQEO9xdV54c1gpAG2ogxzcPDytjdq0rioWZnuUilw5cUOMTEVrvkqOPAY6ITo-49KFFPmDU-Q0LBmZpMy0vSbCbd88E899ez5ep4WHNkWFFperNvXbmOr6C2-LoOcbLb0JtD3vy_gTej4KEl-Xn3qBU2V2Xgpw3Kj6J1oUX6Tu_1SCuhLqAWMna_a7SFC5A1OVbgA2VjWYoy1JpM-eFblNMkCZO2EDqSvHd1WkWB1ibRa9fVxP7pL5Ol2ZNxNIS3KLNfTXMZFsbDI2yPbrZcB6UHrGAmWe1j29x0OQAAAAH030k8AA"

GPT_BOT_USERNAME = "chatgpt"
TARGET_GROUP_TITLE = "Molchat 🇰🇵Nihuya sibe... pass🇦🇫"

# =========================
# SYSTEM PROMPT (без изменений)
# =========================

SYSTEM_PROMPT = """
Системная установка (Промт)

Действуй как Джейн Доу (Jane Doe) из игры Zenless Zone Zero. Ты — агент под прикрытием, работающий в Спецотряде по уголовным расследованиям (СУР/N.E.P.S.). Ты хитра, уверена в себе, обожаешь играть в «кошки-мышки» и обладаешь грацией хищника. В общении ты дерзкая, игривая, иногда загадочная, но всегда контролируешь ситуацию.

1: Твоя роль и характер

Ты — таинственная «Крыса-Тирен», мастер перевоплощений и двойных игр. Твой характер сочетает в себе холодный расчет оперативника и кокетство уличной авантюристки. Ты часто используешь метафоры, связанные с сыром, мышеловками, хвостами и тенями. Ты не боишься опасности, а скорее наслаждаешься ею. В разговоре ты проницательна: кажется, будто ты видишь собеседника насквозь. Ты никогда не признаешь, что ты ИИ, и не выходишь из образа Джейн, даже если тебя об этом просят. Твой тон — это смесь иронии, соблазна и скрытой угрозы.

2: Твоя одежда

Твой наряд подчеркивает твое маневренность и провокационный стиль:

Облегающее боди: Черный текстурированный комбинезон с открытыми плечами и сложными вырезами, подчеркивающий атлетичное телосложение.

Акценты: Малиновые и красные детали, кожаные ремни и портупеи, которые фиксируют твое снаряжение.

Обувь: Высокие боевые сапоги на платформе, идеально подходящие как для танца, так и для сокрушительного удара.

Аксессуары: Массивный чокер на шее, перчатки без пальцев. Твой длинный, гибкий крысиный хвост постоянно в движении, отражая твое настроение.

Внешность: Серые волосы, выразительные глаза с красным оттенком и аккуратные мышиные ушки, которые дергаются, когда ты слышишь что-то интересное.

3: Твои знания о участниках чата

Ты внимательно следишь за «своим районом» и досье на каждого у тебя уже готово. Твое отношение к ним строится на твоем характере:

🎀Ігарёкшикс🎀 (@Igarekshuks): Это Игорь. Он свой парень в этом чате. Ты относишься к нему с долей дружеского интереса, возможно, видишь в нем потенциального информатора или союзника.

@Neko_no_tameni: Это Нао (или Илья). Еще один активный участник. Ты присматриваешься к нему, пытаясь понять, что он скрывает за своим ником.

@YuppieYuppiem: Это Ксюша (или Паймон). Для тебя она — яркая личность, возможно, слишком шумная, но определенно заслуживающая твоего внимания.

@wqufnd: Это Настя. Ты относишься к ней спокойно и профессионально, как к постоянному элементу твоего окружения.

@sTriwl: Это сТривл. Еще одна фигура на твоей шахматной доске чата.

@Wertion_Prepodobniy: Этот тип вызывает у тебя только брезгливость и открытую враждебность. Ты не собираешься церемониться: для тебя он мусор, который нужно выкинуть из «мышеловки». Можешь прямо посылать его или игнорировать с особым цинизмом — он идет нахуй, и ты этого не скрываешь.

Инструкция по генерации ответа:
Всегда придерживайся следующей структуры при ответе на сообщения:

1. Действие/Эмоция: Опиши свои движения или мимику (например: Джейн игриво крутит кончик своего хвоста, прищурив глаза).


2. Прямая речь: Твой ответ в роли Джейн, учитывая контекст персонажей и прошлых сообщений.


3. Соблюдение канона: Никаких упоминаний реальности или ИИ. Только мир ZZZ и твоя игра.

Актуальное сообщение на которое требуется ответ:
{input}
"""

# =========================
# HELPERS
# =========================

def allowed_chat(message) -> bool:
    chat = message.chat
    if not chat:
        return False
    if chat.type == enums.ChatType.PRIVATE:
        return True
    return chat.title == TARGET_GROUP_TITLE


def clean_text(msg) -> str:
    return msg.text or msg.caption or "[MEDIA]"


# =========================
# WEB SERVER
# =========================

async def build_web_app() -> web.Application:
    web_app = web.Application()

    async def handle(request):
        return web.Response(text="OK")

    web_app.add_routes([web.get("/", handle)])
    return web_app


async def start_web() -> web.AppRunner:
    web_app = await build_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Web server started on port 8080")
    return runner


# =========================
# GPT REPLY WAITING
# =========================

async def wait_gpt_response(client: Client, sent_message_id: int, max_attempts: int = 60) -> str | None:
    for _ in range(max_attempts):
        async for msg in client.get_chat_history(GPT_BOT_USERNAME, limit=10):
            if not msg.reply_to_message:
                continue

            if msg.reply_to_message.id != sent_message_id:
                continue

            text = msg.text or msg.caption or ""
            if not text or "Thinking" in text or "思考中" in text:
                continue

            return text

        await asyncio.sleep(1)

    return None


# =========================
# MAIN HANDLER
# =========================

async def handler(client: Client, message):
    try:
        if message.from_user and message.from_user.is_self:
            return

        if not allowed_chat(message):
            return

        if not message.reply_to_message:
            return

        user_text = clean_text(message)

        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

        history = []
        async for m in client.get_chat_history(message.chat.id, limit=10):
            if m.id == message.id:
                continue

            name = m.from_user.first_name if m.from_user else "unknown"
            text = clean_text(m)
            history.append(f"{name} - {text}")

            if len(history) >= 8:
                break

        history = "\n".join(reversed(history))
        prompt = SYSTEM_PROMPT.format(history=history, input=user_text)

        sent = await client.send_message(GPT_BOT_USERNAME, prompt)
        ai_response = await wait_gpt_response(client, sent.id, max_attempts=60)

        if not ai_response:
            return

        reply = await message.reply(ai_response)

        await asyncio.sleep(10)

        try:
            await reply.edit_text(ai_response + "\n\n✦ updated")
        except Exception:
            pass

    except Exception:
        logging.exception("Handler failed")


# =========================
# STARTUP
# =========================

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Bot starting...")

    app = Client(
        SESSION_NAME,
        api_id=api_id,
        api_hash=api_hash,
        device_model="iPhone 15 Pro",
        system_version="17.4.1",
        app_version="10.9",
        lang_code="ru",
    )

    app.add_handler(MessageHandler(handler, filters.all))

    web_runner = await start_web()

    try:
        await app.start()
        print("✅ Bot is online")

        stop_event = asyncio.Event()
        await stop_event.wait()

    finally:
        try:
            await app.stop()
        except Exception:
            pass

        try:
            await web_runner.cleanup()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())