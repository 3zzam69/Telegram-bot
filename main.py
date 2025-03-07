import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
bot = telebot.TeleBot(TOKEN)

# تخزين بيانات المستخدمين
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id in user_data and user_data[user_id]['step'] >= 6:
        bot.send_message(user_id, "أنت مسجل بالفعل! يمكنك الآن إرسال حلمك وسأساعدك في تفسيره.")
        return

    user_data[user_id] = {'step': 1}
    bot.send_message(user_id, "أهلاً بك! لنبدأ بجمع بعض المعلومات عنك. ما اسمك الثلاثي؟")

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip()

    if user_id not in user_data:
        return

    step = user_data[user_id]['step']

    if step == 1:  # التحقق من الاسم
        if is_valid_name(text):
            user_data[user_id]['name'] = text
            bot.send_message(user_id, "كم عمرك؟")
            user_data[user_id]['step'] = 2
        else:
            bot.send_message(user_id, "⚠️ الرجاء إدخال اسمك الثلاثي بشكل صحيح دون أرقام أو رموز.")

    elif step == 2:  # التحقق من العمر
        if text.isdigit() and 10 <= int(text) <= 120:
            user_data[user_id]['age'] = int(text)
            send_marital_status_options(user_id)  # عرض أزرار الحالة الاجتماعية
            user_data[user_id]['step'] = 3
        else:
            bot.send_message(user_id, "⚠️ الرجاء إدخال عمرك الصحيح (بين 10 و 120 سنة).")

    elif step == 4:  # التحقق من عدد أفراد الأسرة
        if text.isdigit() and 1 <= int(text) <= 50:
            user_data[user_id]['family_members'] = int(text)
            send_religious_level_options(user_id)  # عرض أزرار الالتزام الديني
            user_data[user_id]['step'] = 5
        else:
            bot.send_message(user_id, "⚠️ الرجاء إدخال عدد أفراد الأسرة الصحيح (بين 1 و 50).")

    elif step == 6:  # استقبال الحلم
        user_data[user_id]['dream'] = text
        analyze_dream(user_id)

# التحقق من صحة الاسم الثلاثي
def is_valid_name(name):
    words = name.split()
    if len(words) < 3:
        return False
    for word in words:
        if not word.isalpha() or not word.isascii():
            return False
    return True

# إرسال أزرار اختيار الحالة الاجتماعية
def send_marital_status_options(user_id):
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("أعزب", callback_data="marital_أعزب"),
        InlineKeyboardButton("متزوج", callback_data="marital_متزوج"),
        InlineKeyboardButton("مطلق", callback_data="marital_مطلق"),
        InlineKeyboardButton("أرمل", callback_data="marital_أرمل")
    ]
    markup.add(*buttons)
    bot.send_message(user_id, "ما حالتك الاجتماعية؟", reply_markup=markup)

# إرسال أزرار اختيار الالتزام الديني
def send_religious_level_options(user_id):
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("مرتفع", callback_data="religious_مرتفع"),
        InlineKeyboardButton("متوسط", callback_data="religious_متوسط"),
        InlineKeyboardButton("منخفض", callback_data="religious_منخفض")
    ]
    markup.add(*buttons)
    bot.send_message(user_id, "ما مدى التزامك الديني؟", reply_markup=markup)

# التعامل مع الردود من الأزرار الشفافة
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    data = call.data

    if data.startswith("marital_"):  # حالة اجتماعية
        choice = data.split("_")[1]
        user_data[user_id]['marital_status'] = choice
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f"💍 حالتك الاجتماعية: {choice}")
        bot.send_message(user_id, "كم عدد أفراد أسرتك؟")
        user_data[user_id]['step'] = 4

    elif data.startswith("religious_"):  # الالتزام الديني
        choice = data.split("_")[1]
        user_data[user_id]['religious_level'] = choice
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f"🕌 مستوى التزامك الديني: {choice}")
        bot.send_message(user_id, "شكراً لك! الآن يمكنك إرسال حلمك وسأساعدك في تفسيره.")
        user_data[user_id]['step'] = 6

# تحليل الحلم وعرض البيانات
def analyze_dream(user_id):
    user = user_data[user_id]
    response = f"🔍 تحليل حلمك بناءً على بياناتك:\n"
    response += f"👤 الاسم: {user['name']}\n"
    response += f"🎂 العمر: {user['age']}\n"
    response += f"💍 الحالة الاجتماعية: {user['marital_status']}\n"
    response += f"🏠 عدد أفراد الأسرة: {user['family_members']}\n"
    response += f"🕌 الالتزام الديني: {user['religious_level']}\n\n"
    response += f"🛌 الحلم: {user['dream']}\n"
    response += f"📌 التفسير: جارٍ التحليل بناءً على معلوماتك الشخصية..."

    bot.send_message(user_id, response)

bot.polling()
