import asyncio
import os
from datetime import datetime
from aiohttp import web

# === ПАТЧ ДЛЯ RENDER И НОВЫХ ВЕРСИЙ PYTHON ===
# Создаем event loop ДО импорта pyrogram, чтобы он не крашился при инициализации
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ==============================================

from pyrogram import Client, filters, enums

# === Твои данные (вшиты намертво) ===
API_ID = 36448320
API_HASH = "6794e24f29aa879cf1a067cfc230c330"
SESSION_STRING = "BAIsKEAAtqTAKfba-wSpQbFOKE6B4CciFF-f7aqtvx-oMQy8mBLqN5ThRQEO9xdV54c1gpAG2ogxzcPDytjdq0rioWZnuUilw5cUOMTEVrvkqOPAY6ITo-49KFFPmDU-Q0LBmZpMy0vSbCbd88E899ez5ep4WHNkWFFperNvXbmOr6C2-LoOcbLb0JtD3vy_gTej4KEl-Xn3qBU2V2Xgpw3Kj6J1oUX6Tu_1SCuhLqAWMna_a7SFC5A1OVbgA2VjWYoy1JpM-eFblNMkCZO2EDqSvHd1WkWB1ibRa9fVxP7pL5Ol2ZNxNIS3KLNfTXMZFsbDIy3pbrZcB6UHrGAmWe1j29x0OQAAAAH030k8AA"

# === Настройки ===
GPT_BOT_USERNAME = "chatgpt"  # Юзернейм бота для обработки запросов
gpt_all_enabled = False       # Глобальный переключатель

# === СИСТЕМНАЯ РОЛЬ (Промпт) ===
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
3. Соблюдение канона: Никаких упоминаний реальности или ИИ. Только мир ZZZ и твоя игра но! писать структцрц не надо. только ответ на сообщение и действие в звездочках. без лишней структуры.
"""

# === Настройка клиента ===
app = Client(
    "jane_doe_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    device_model="iPhone 15 Pro",
    system_version="17.4.1",
    app_version="10.9",
    lang_code="ru"
)

# === Команда /GptAll (Вкл/Выкл) ===
@app.on_message(filters.command("GptAll", prefixes="/") & filters.me)
async def toggle_gpt_handler(client, message):
    global gpt_all_enabled
    gpt_all_enabled = not gpt_all_enabled
    status = "ВКЛЮЧЕН ✅" if gpt_all_enabled else "ВЫКЛЮЧЕН ❌"
    await message.edit_text(f"🐀 Режим Jane Doe для всех ЛС: {status}")
    print(f"Режим GptAll: {status}")

# === Основной обработчик ЛС ===
@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def handle_private_messages(client, message):
    global gpt_all_enabled

    if not gpt_all_enabled:
        return

    chat_id = message.chat.id
    sender_name = message.from_user.first_name if message.from_user else "Неизвестный"
    sender_username = f"@{message.from_user.username}" if message.from_user and message.from_user.username else ""

    # Идентификатор для промпта
    user_id_str = f"{sender_name} ({sender_username})" if sender_username else sender_name

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

        if hist_msg.from_user.is_self:
            history_messages.append(f"(Джейн Доу - {h_text})")
        else:
            h_name = hist_msg.from_user.first_name if hist_msg.from_user else "Неизвестный"
            history_messages.append(f"({h_name} - {h_text})")

        if len(history_messages) >= 6:
            break

    history_block = "\n".join(reversed(history_messages))

    full_query = (
        f"{SYSTEM_PROMPT}\n\n"
        f"[Прошлые сообщения]\n{history_block}\n\n"
        f"Актуальное сообщение на которое требуется ответ:\n"
        f"[{user_id_str}]: {user_text}"
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
                if not bot_msg.from_user.is_self:
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

# === Фейковый веб-сервер для Render / UptimeRobot ===
async def keep_alive_server():
    async def handle_request(request):
        return web.Response(text="Jane Doe is watching...")

    web_app = web.Application()
    web_app.router.add_get('/', handle_request)
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    # Render автоматически задает переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Веб-сервер запущен на порту {port}. Порты открыты для Render/UptimeRobot.")

# === Запуск ===
async def main():
    print("🚀 Запуск Jane Doe Userbot (Render Mode)...")
    await keep_alive_server() # Поднимаем порты
    
    async with app:
        print("✅ Бот в сети. Команда активации: /GptAll")
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
