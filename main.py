import time
import telebot

# استبدل هذا بالتوكن الخاص بك
TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
bot = telebot.TeleBot(TOKEN)

# معرف الشات الذي تريد إرسال رسالة إليه عند تشغيل البوت
CHAT_ID = "1487998139"

# إرسال رسالة ترحيبية واحدة فقط عند تشغيل البوت
bot.send_message(CHAT_ID, "✅ مبروك! البوت يعمل الآن بنجاح!")

# دالة لمعالجة الأوامر والرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا بك! البوت يعمل بنجاح 🎉")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"📩 لقد أرسلت: {message.text}")

# تشغيل البوت
print("✅ البوت يعمل الآن...")
bot.infinity_polling()
