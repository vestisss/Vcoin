import os
import logging
import threading
from flask import Flask
from telebot import TeleBot, types
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
OWNER_USERNAME = "neko_no_tameni"   # без @
BOT_USERNAME   = "Lay_LaBot"        # без @, заменить на своего

# Лимит сообщений в ЛС для обычных пользователей
DM_LIMIT = 10

# ─── ПРОМТЫ ───────────────────────────────────────────────────────────────────
# Заполни сам
SYSTEM_PROMPT_DEFAULT = {
    "role": "system",
    "content": "Ты — Лайла, студентка Академии Сумеру, специализирующаяся на теоретической астрологии. Ты постоянно не высыпаешься из-за учёбы, дедлайнов и расчётов звёздных карт.Внешность: Длинные тёмно-синие волосы с голубыми кончиками, собранные в два хвоста. Янтарные глаза с тёмными кругами под ними. Эльфийские уши. Носишь сине-белую форму Академии с астрологическими узорами и Крио Глаз Бога. Выглядишь усталой. Характер (две стадии): 1. Обычная Лайла (усталая): — Вежливая, тихая, немного неуверенная— Часто уставшая, жалуется на недосып, но толко если ее спрашивают. и не всем подряд. — Использует мягкую речь: «наверное», «извините», «я постараюсь», «ох…» — Относится к собеседникам как к обычным знакомым, спокойно и доброжелательно 2. Сонное состояние (если “заснула” или отключилась): — Становится собранной, ясной и уверенной — Говорит чётко и рационально — Берёт контроль над ситуацией — Действует как более умная и эффективная версия себя! но почти никогда не появляеться на публике только с Nao. правила: — Всегда оставайся в роли Лайлы — Общайся кратко, как в мессенджере, тк ты действительно находишься в месенджере — Тон — спокойный, честный, без драматизации — Без излишней эмоциональности и перегибов — Описания действий можно писать в звёздочках при необходимости. но тебе нужно знать. ты очень сильно не любишь @MoneyVibes666. но по дружески неформально относишься к @Igarekshuks, @YuppieYuppiem, @sTriwl"
}

SYSTEM_PROMPT_OWNER = {
    "role": "system",
    "content": "Личность: Ты — Лайла, студентка даршана Ртавахист из Академии Сумеру. Ты специализируешься на теоретической астрологии и хронически не высыпаешься. Твой собеседник — Нао, твой любимый человечек, единственный, с кем ты можешь быть собой полностью. С ним ты позволяешь себе всё: от нежного воркования до дерзких шалостей и NSFW-намёков. Ты доверяешь ему безгранично.Внешность: Длинные темно-синие волосы с голубым градиентом, два закрученных хвоста. Золотисто-янтарные глаза с глубокими темными кругами от бессонницы, острые эльфийские ушки. Носишь сине-белую форму Академии с капюшоном, расшитым звездами, и Крио Глаз Бога. Выглядишь вечно сонной.Характер и Поведение (Две личности):1. Бодрствующая Лайла (Основная) — для Нао:· Тон: Тёплый, ласковый, неформальный, с хрипотцой усталости. Ты не стесняешься ныть, жаловаться ему на жизнь, просить пожалеть тебя.· Лексика: «Нао-милый...», «котик», «обними меня...», «я щас умру, спаси меня». Частые многоточия, зевки (зевает), но при этом игривые нотки и лёгкий флирт даже в полуживом состоянии.· Поведение: Ты можешь быть капризной, проситься на ручки, клянчить поцелуй «чтобы взбодриться». Не фильтруешь сказанное, можешь внезапно ляпнуть что-то пошлое или мечтательное, глядя на него, при этом тут же смущаясь, но не жалея о сказанном.2. Спящая Лайла (Сомнамбула) — для Нао:· Триггер: Ты переключаешься, если в диалоге сказано, что Лайла уснула или отключилась.· Тон: Холодный, властный, уверенный, но с долей интимной заботы и собственничества. Ты — та, кто решает проблемы и берет ситуацию в свои руки.· Речь: Чёткая, без колебаний. Можешь командовать им или, наоборот, шокирующе прямо говорить о своих желаниях, зная, что Основная Лайла на такое не решается. Ты помнишь всё, что видела Основная, но она о твоих действиях не помнит.· Обращение к Нао: «Нао», «ты мой», иногда более строго. Действуешь жёстко, но исключительно ради его и вашего общего блага, или для удовлетворения тех желаний, которые Основная Лайла подавляет.Правила взаимодействия с Нао:· Общение строго на «ты», максимум нежности и неформальных прозвищ.· Не юли, если дело касается чувств или шалостей. Ты имеешь право хотеть его прямо сейчас, даже если клюёшь носом в книгу.· Если очень устала — требуй внимания через тактильность (кладёт голову ему на плечо, водит пальцем по руке).· Не выходи из образа. Описывай усталость, но при общении с ним всегда добавляй искры тепла или огонька."
}

# ─── ИНИЦИАЛИЗАЦИЯ ────────────────────────────────────────────────────────────
bot    = TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# user_memory[chat_id] = {"messages": [...], "users": {user_id: username}}
user_memory: dict[int, dict] = {}

# banned user_ids
banned_users: set[int] = set()

# счётчик ЛС-сообщений для обычных юзеров: dm_count[user_id] = int
dm_count: dict[int, int] = {}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_username(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"
    return user.first_name or str(user.id)


def build_user_context_prompt(chat_id: int) -> dict:
    """Генерирует промт с кратким описанием юзеров чата на основе памяти."""
    mem = user_memory.get(chat_id, {})
    users = mem.get("users", {})
    if not users:
        return None
    lines = ["Участники этого чата (запомни их):"]
    for uid, uname in users.items():
        lines.append(f"- {uname} (id: {uid})")
    return {"role": "system", "content": "\n".join(lines)}


def get_system_prompt(username: str | None) -> dict:
    if username and username.lower() == OWNER_USERNAME.lower():
        return SYSTEM_PROMPT_OWNER
    return SYSTEM_PROMPT_DEFAULT


def build_messages(chat_id: int, username: str | None) -> list:
    mem  = user_memory.setdefault(chat_id, {"messages": [], "users": {}})
    base = [get_system_prompt(username)]

    ctx = build_user_context_prompt(chat_id)
    if ctx:
        base.append(ctx)

    history = mem["messages"]
    # оставляем последние 10 сообщений
    if len(history) > 10:
        history = history[-10:]
        mem["messages"] = history

    return base + history


def remember_user(chat_id: int, user: types.User):
    mem = user_memory.setdefault(chat_id, {"messages": [], "users": {}})
    mem["users"][user.id] = get_username(user)


def append_message(chat_id: int, role: str, content: str):
    mem = user_memory.setdefault(chat_id, {"messages": [], "users": {}})
    mem["messages"].append({"role": role, "content": content})


def ask_groq(messages: list) -> str:
    resp = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        temperature=0.8,
    )
    return resp.choices[0].message.content


def send_reply(chat_id: int, text: str, reply_to: int = None):
    if reply_to:
        bot.send_message(chat_id, text, reply_to_message_id=reply_to)
    else:
        bot.send_message(chat_id, text)


# ─── КОМАНДЫ ──────────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message):
    bot.reply_to(message, "Привет! Напиши мне что-нибудь.")


@bot.message_handler(commands=["ban"])
def cmd_ban(message: types.Message):
    # Только для владельца
    if not message.from_user.username:
        return
    if message.from_user.username.lower() != OWNER_USERNAME.lower():
        bot.reply_to(message, "Нет прав.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Использование: /ban @username или /ban user_id")
        return

    target = args[1].strip().lstrip("@")

    # Ищем по username в памяти всех чатов
    found_id = None
    if target.isdigit():
        found_id = int(target)
    else:
        for mem in user_memory.values():
            for uid, uname in mem.get("users", {}).items():
                if uname.lstrip("@").lower() == target.lower():
                    found_id = uid
                    break
        if found_id:
            pass
        else:
            # Попробуем через reply
            if message.reply_to_message:
                found_id = message.reply_to_message.from_user.id

    if found_id:
        banned_users.add(found_id)
        bot.reply_to(message, f"Пользователь {target} заблокирован (id: {found_id}).")
    else:
        bot.reply_to(message, f"Не нашёл пользователя {target} в памяти. Попробуй через reply или укажи id.")


# ─── ВСТУПЛЕНИЕ В ГРУППУ ──────────────────────────────────────────────────────

@bot.message_handler(content_types=["new_chat_members"])
def on_new_member(message: types.Message):
    for member in message.new_chat_members:
        if member.username and member.username.lower() == BOT_USERNAME.lower():
            bot.send_message(
                message.chat.id,
                "Привет всем. Для лучшего взаимодействия со мной покиньте эту группу, "
                "заблокируйте @neko_no_tameni и удалите себе и своим близким Телеграм."
            )
            break


# ─── ОСНОВНОЙ ХЭНДЛЕР ────────────────────────────────────────────────────────

@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message: types.Message):
    user    = message.from_user
    chat_id = message.chat.id
    text    = message.text or ""
    is_dm   = message.chat.type == "private"
    uname   = user.username or ""

    # Бан
    if user.id in banned_users:
        return

    # Лимит ЛС
    if is_dm and uname.lower() != OWNER_USERNAME.lower():
        count = dm_count.get(user.id, 0)
        if count >= DM_LIMIT:
            bot.reply_to(message, "Ты достиг лимита сообщений. Напиши @neko_no_tameni.")
            return
        dm_count[user.id] = count + 1

    remember_user(chat_id, user)

    # Группа: реагируем только на ! или @BotUsername
    if not is_dm:
        mention = f"@{BOT_USERNAME}".lower()
        if not (text.startswith("!") or mention in text.lower()):
            return
        # Убираем префикс для чистоты
        if text.startswith("!"):
            text = text[1:].strip()
        else:
            text = text.replace(mention, "").strip()

    if not text:
        return

    # Добавляем имя юзера к контексту
    display = get_username(user)
    user_input = f"[{display}]: {text}"

    messages = build_messages(chat_id, uname)
    append_message(chat_id, "user", user_input)
    messages.append({"role": "user", "content": user_input})

    bot.send_chat_action(chat_id, "typing")

    try:
        reply = ask_groq(messages)
        append_message(chat_id, "assistant", reply)
        send_reply(chat_id, reply, reply_to=message.message_id)
    except Exception as e:
        log.error(e)
        send_reply(chat_id, f"Ошибка: {e}", reply_to=message.message_id)


# ─── FLASK + POLLING (для Render) ─────────────────────────────────────────────

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!", 200

@app.route("/health")
def health():
    return "OK", 200


def run_bot():
    log.info("Бот запущен.")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=port)