import telebot
from flask import Flask, request
import os
import requests

# ✅ احصل على التوكن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")  # ضع التوكن في GitHub Secrets أو Railway Variables
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ضع رابط Railway في GitHub Secrets

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ✅ تعريف نقطة استقبال Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# ✅ أمر /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "🚀 أهلاً بك! البوت يعمل بنجاح.")

# ✅ أمر /help
@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, "❓ استخدم الأوامر المتاحة للتفاعل مع البوت.")

# ✅ استجابة لأي رسالة نصية
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, f"📩 لقد قلت: {message.text}")

# ✅ تشغيل التطبيق على Railway
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
