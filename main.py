import os
import telebot
from flask import Flask, request

# تعريف متغيرات البيئة
TOKEN = "79ab4694-7487-48b1-9a09-29bf8c162d7b"  # ضع توكن البوت الخاص بك هنا
WEBHOOK_URL = "https://web-production-9475.up.railway.app"  # رابط Railway الخاص بك

# إنشاء كائن البوت
bot = telebot.TeleBot(TOKEN)

# إنشاء تطبيق Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "بوت تيليجرام يعمل بنجاح 🚀"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """ استقبال الطلبات من تيليجرام """
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أنا بوت تيليجرام يعمل عبر Railway 🚀")

# تشغيل Webhook عند بدء التطبيق
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 5000))  # استخدام PORT من بيئة Railway
    app.run(host="0.0.0.0", port=port)
