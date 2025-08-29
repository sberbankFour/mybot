import telebot
import os

# === Настройки ===
TOKEN = "8381752423:AAF_2I5FKp6qzBOJ0sA4PTkh6c_vsazsEpA"
OWNER_ID = 6833868015  # твой Telegram ID
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# словарь для связи сообщений владельца и пользователей
user_map = {}  # msg_id владельца → id пользователя

# --- Старт с приветствием ---
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    photo_path = os.path.join("mybot", "photo.jpg")  # имя файла с фото, если есть
    caption_text = (
        "—  при̲ве̲т̲ :  ׄ  𓈒  𝆹𝅥 опиши\n"
        "𝆭   свою проблему или предложение  ᷼  𓆩    𓈒   ͡   ͡   "
    )
    if os.path.exists(photo_path):
        bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=caption_text)
    else:
        bot.send_message(chat_id, caption_text)

# --- Обработка сообщений ---
@bot.message_handler(func=lambda message: True, content_types=['text','photo','document','sticker','video','voice','audio','animation'])
def handle_message(message):
    user_id = message.from_user.id

    # если пишет не владелец
    if user_id != OWNER_ID:
        # отправляем уведомление пользователю
        bot.reply_to(message, "сообщение будет рассмотрено в скором времени")

        # уведомление владельцу
        header = "⇄ нв͞о͞ая уведомление . . ▭꯭۫͡▬۫ ִ ִ▭  "
        if message.content_type == 'text':
            sent = bot.send_message(OWNER_ID, f"{header}\n{message.text}")
        else:
            bot.send_message(OWNER_ID, header)
            sent = bot.copy_message(OWNER_ID, message.chat.id, message.message_id)

        # сохраняем связь msg_id владельца → id пользователя
        user_map[sent.message_id] = user_id

    else:
        # владелец отвечает пользователю
        if message.reply_to_message and message.reply_to_message.message_id in user_map:
            target_id = user_map[message.reply_to_message.message_id]
            # пересылаем любой тип контента
            if message.content_type == 'text':
                bot.send_message(target_id, f"⇄ новое уве̼д̼о̼м̼л̼е̼н̼и̼е . . ▭꯭۫͡▬۫ ִ ִ▭  \n{message.text}")
            else:
                bot.copy_message(target_id, message.chat.id, message.message_id)
            bot.reply_to(message, "ответ отправлен")
        else:
            bot.reply_to(message, "отправь ответ человеку свайпом вправо")

print("Бот запущен 🚀")
bot.infinity_polling(skip_pending=True)