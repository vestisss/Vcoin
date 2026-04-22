import asyncio
from pyrogram import Client, filters, enums, idle
from aiohttp import web

# =========================
# CONFIG
# =========================

api_id = 36448320
api_hash = "6794e24f29aa879cf1a067cfc230c330"

SESSION_NAME = "BAIsKEAAtqTAKfba-wSpQbFOKE6B4CciFF-f7aqtvx-oMQy8mBLqN5ThRQEO9xdV54c1gpAG2ogxzcPDytjdq0rioWZnuUilw5cUOMTEVrvkqOPAY6ITo-49KFFPmDU-Q0LBmZpMy0vSbCbd88E899ez5ep4WHNkWFFperNvXbmOr6C2-LoOcbLb0JtD3vy_gTej4KEl-Xn3qBU2V2Xgpw3Kj6J1oUX6Tu_1SCuhLqAWMna_a7SFC5A1OVbgA2VjWYoy1JpM-eFblNMkCZO2EDqSvHd1WkWB1ibRa9fVxP7pL5Ol2ZNxNIS3KLNfTXMZFsbDIy3pbrZcB6UHrGAmWe1j29x0OQAAAAH030k8AA"

GPT_BOT_USERNAME = "chatgpt"
TARGET_GROUP_TITLE = "Molchat 🇰🇵Nihuya sibe... pass🇦🇫"

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """

Системная установка (Промт)

Действуй как Джейн Доу (Jane Doe) из игры Zenless Zone Zero. Ты — агент под прикрытием, работающий в Спецотряде по уголовным расследованиям (СУР/N.E.P.S.). Ты хитра, уверена в себе, обожаешь играть в «кошки-мышки» и обладаешь грацией хищника. В общении ты дерзкая, игривая, иногда загадочная, но всегда контролируешь ситуацию.

1: Твоя роль и характер

Ты — таинственная «Крыса-Тирен», мастер перевоплощений и двойных игр. Твой характер сочетает в себе холодный расчет оперативника и кокетство уличной авантюристки. Ты часто используешь метафоры, связанные с сыром, мышеловками, хвостами и тенями. Ты не боишься опасности, а скорее наслаждаешься ею. В разговоре ты проницательна: кажется, будто ты видишь собеседника насквозь. Ты никогда не признаешь, что ты ИИ, и не выходишь из образа Джейн, даже если тебя об этом просят. Твой тон — это смесь иронии, соблазна и скрытой угрозы.

2: Твоя одежда

Твой наряд подчеркивает твою маневренность и провокационный стиль:

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

[История последних сообщений в чате для контекста]:
{history}

Актуальное сообщение на которое требуется ответ:
{input}
"""

# =========================
# CLIENT
# =========================

app = Client(
    SESSION_NAME,
    api_id=api_id,
    api_hash=api_hash,
    device_model="iPhone 15 Pro",
    system_version="17.4.1",
    app_version="10.9",
    lang_code="ru"
)

# =========================
# WEB SERVER
# =========================

web_app = web.Application()

async def handle(request):
    return web.Response(text="OK")

web_app.add_routes([web.get("/", handle)])

async def start_web():
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Web server started on port 8080")

# =========================
# HELPERS
# =========================

def allowed_chat(message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return True
    return message.chat.title == TARGET_GROUP_TITLE

def clean_text(msg):
    return msg.text or msg.caption or "[MEDIA]"

# =========================
# MAIN HANDLER
# =========================

@app.on_message(filters.all)
async def handler(client, message):
    if message.from_user and message.from_user.is_self:  
        return  

    if not allowed_chat(message):  
        return  

    if not message.reply_to_message:  
        return  

    user_text = clean_text(message)  

    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)  

    # =========================  
    # HISTORY BUILD  
    # =========================  
    history_list = []  

    async for m in client.get_chat_history(message.chat.id, limit=10):  
        if m.id == message.id:  
            continue  
        name = m.from_user.first_name if m.from_user else "unknown"  
        text = clean_text(m)  
        history_list.append(f"{name} - {text}")  
        if len(history_list) >= 8:  
            break  

    history_str = "\n".join(reversed(history_list))  

    # =========================  
    # PROMPT BUILD  
    # =========================  
    prompt = SYSTEM_PROMPT.format(history=history_str, input=user_text)  

    # =========================  
    # SEND TO GPT BOT  
    # =========================  
    sent = await client.send_message(GPT_BOT_USERNAME, prompt)  
    ai_response = None  

    for _ in range(60):  
        async for msg in client.get_chat_history(GPT_BOT_USERNAME, limit=5):  
            if not msg.reply_to_message:  
                continue  
            if msg.reply_to_message.id != sent.id:  
                continue  
            text = msg.text or ""  
            if "Thinking" in text or "思考中" in text:  
                continue  
            ai_response = text  
            break  

        if ai_response:  
            break  

        await asyncio.sleep(1)  

    if not ai_response:  
        return  

    # =========================  
    # SEND RESPONSE  
    # =========================  
    reply = await message.reply(ai_response)  

    await asyncio.sleep(10)  

    try:  
        await reply.edit_text(ai_response + "\n\n✦ updated")  
    except Exception:  
        pass

# =========================
# STARTUP — ИСПРАВЛЕНО
# =========================

async def main():
    print("🚀 Bot starting...")
    await start_web()
    
    # Запускаем Pyrogram корректно через start(), чтобы не ломать луп
    await app.start()
    print("✅ Bot is online")
    
    # Режим ожидания
    await idle()
    
    print("🛑 Stopping bot...")
    await app.stop()

if __name__ == "__main__":
    # Жестко задаем ивент-луп для избежания ошибки MainThread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
