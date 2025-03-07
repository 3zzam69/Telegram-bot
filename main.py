from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
import time

API_ID = 27155532  # ضع API_ID هنا
API_HASH = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"  # ضع API_HASH هنا
BOT_TOKEN = "4b49a9b7bc41ad7f3c66d88a47f24ecc"  # ضع توكن البوت هنا

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

CHANNEL_USERNAME = "Non_Arab"  # ضع معرف القناة بدون @

def is_user_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"خطأ أثناء التحقق من الاشتراك: {e}")
        return False

@bot.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id

    while not is_user_subscribed(user_id):
        message.reply_text(f"🔴 **يجب عليك الاشتراك في القناة لاستخدام البوت!**\n"
                           f"👉 [اضغط هنا للاشتراك](https://t.me/{CHANNEL_USERNAME}) ثم أرسل /start مرة أخرى.",
                           disable_web_page_preview=True)
        
        time.sleep(10)  # انتظار 10 ثوانٍ قبل إعادة التحقق

    message.reply_text("✅ **أهلا بك! تم التحقق من اشتراكك بنجاح. يمكنك الآن استخدام البوت.**")

bot.run()