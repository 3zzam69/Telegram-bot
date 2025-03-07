import telebot

TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
bot = telebot.TeleBot(TOKEN)

# تخزين بيانات المستخدمين
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 1}  # بدء جمع البيانات
    bot.send_message(user_id, "أهلاً بك! لنبدأ بجمع بعض المعلومات عنك. ما اسمك الثلاثي؟")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip()

    if user_id in user_data:
        step = user_data[user_id]['step']

        if step == 1:  # الاسم الثلاثي
            user_data[user_id]['name'] = text
            bot.send_message(user_id, "كم عمرك؟")
            user_data[user_id]['step'] = 2

        elif step == 2:  # العمر
            if text.isdigit():
                user_data[user_id]['age'] = int(text)
                bot.send_message(user_id, "ما حالتك الاجتماعية؟ (أعزب / متزوج / مطلق / أرمل)")
                user_data[user_id]['step'] = 3
            else:
                bot.send_message(user_id, "الرجاء إدخال عمرك بالأرقام فقط.")

        elif step == 3:  # الحالة الاجتماعية
            if text in ["أعزب", "متزوج", "مطلق", "أرمل"]:
                user_data[user_id]['marital_status'] = text
                bot.send_message(user_id, "كم عدد أفراد أسرتك؟")
                user_data[user_id]['step'] = 4
            else:
                bot.send_message(user_id, "الرجاء اختيار إحدى الإجابات: أعزب / متزوج / مطلق / أرمل.")

        elif step == 4:  # عدد أفراد الأسرة
            if text.isdigit():
                user_data[user_id]['family_members'] = int(text)
                bot.send_message(user_id, "ما مدى التزامك الديني؟ (مرتفع / متوسط / منخفض)")
                user_data[user_id]['step'] = 5
            else:
                bot.send_message(user_id, "الرجاء إدخال عدد أفراد الأسرة بالأرقام فقط.")

        elif step == 5:  # الالتزام الديني
            if text in ["مرتفع", "متوسط", "منخفض"]:
                user_data[user_id]['religious_level'] = text
                bot.send_message(user_id, "شكراً لك! الآن يمكنك إرسال حلمك وسأساعدك في تفسيره.")
                user_data[user_id]['step'] = 6  # جاهز لتلقي الأحلام
            else:
                bot.send_message(user_id, "الرجاء اختيار إحدى الإجابات: مرتفع / متوسط / منخفض.")

        elif step == 6:  # استقبال الحلم
            user_data[user_id]['dream'] = text
            analyze_dream(user_id)  # تحليل الحلم بناءً على المعلومات الشخصية

def analyze_dream(user_id):
    user = user_data[user_id]
    response = f"تحليل حلمك بناءً على بياناتك:\n"
    response += f"👤 الاسم: {user['name']}\n"
    response += f"🎂 العمر: {user['age']}\n"
    response += f"💍 الحالة الاجتماعية: {user['marital_status']}\n"
    response += f"🏠 عدد أفراد الأسرة: {user['family_members']}\n"
    response += f"🕌 الالتزام الديني: {user['religious_level']}\n\n"
    response += f"🛌 الحلم: {user['dream']}\n"
    response += f"📌 التفسير: جارٍ التحليل بناءً على معلوماتك الشخصية..."

    bot.send_message(user_id, response)
    del user_data[user_id]  # مسح البيانات بعد التحليل للحفاظ على الخصوصية

bot.polling()
