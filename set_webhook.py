import requests

TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"  # ضع توكن البوت هنا
WEBHOOK_URL = "https://web-production-9475.up.railway.app"  # رابط Railway الخاص بك

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/{TOKEN}")

print(response.json())  # طباعة استجابة Telegram
