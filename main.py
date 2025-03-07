import os
from flask import Flask

# جلب المتغيرات من البيئة
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# التحقق من وجود القيم
if not TOKEN:
    raise ValueError("🚨 خطأ: متغير البيئة BOT_TOKEN غير مضبوط!")
if not WEBHOOK_URL:
    raise ValueError("🚨 خطأ: متغير البيئة WEBHOOK_URL غير مضبوط!")

print(f"✅ BOT_TOKEN مضبوط: {TOKEN[:10]}...")  # طباعة أول 10 أحرف فقط للتحقق
print(f"✅ WEBHOOK_URL مضبوط: {WEBHOOK_URL}")

# إنشاء تطبيق Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ البوت يعمل بنجاح!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
