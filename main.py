import os
from flask import Flask, request

# جلب التوكن والرابط من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("🚨 خطأ: متغير البيئة BOT_TOKEN غير مضبوط!")
if not WEBHOOK_URL:
    raise ValueError("🚨 خطأ: متغير البيئة WEBHOOK_URL غير مضبوط!")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ البوت يعمل بنجاح!", 200

@app.route("/", methods=["POST"])
def webhook():
    update = request.json
    print(f"📩 تحديث جديد من تيليجرام: {update}")  
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
