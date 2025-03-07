import telebot
from flask import Flask, request

TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🚀 إعداد Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! البوت يعمل الآن عبر Webhook 🚀")

# 📌 تشغيل Flask فقط عند استخدام Railway
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://your-railway-app-url.onrender.com/" + TOKEN)  # ضع رابط Railway هنا
    app.run(host="0.0.0.0", port=5000)
