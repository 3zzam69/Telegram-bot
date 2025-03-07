import os

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("🚨 خطأ: متغير البيئة BOT_TOKEN غير مضبوط!")
if not WEBHOOK_URL:
    raise ValueError("🚨 خطأ: متغير البيئة WEBHOOK_URL غير مضبوط!")

print(f"✅ BOT_TOKEN مضبوط: {TOKEN[:10]}...")  # طباعة أول 10 أحرف فقط للتحقق
print(f"✅ WEBHOOK_URL مضبوط: {WEBHOOK_URL}")
