from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.environ.get("7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8")  # سيتم أخذ التوكن من إعدادات Railway

# ─── وظيفة رد على أمر /start ──────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت يعمل على Railway 🚂")

# ─── تشغيل البوت ──────────────────────────────
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # الطريقة 1: Long Polling (للتجربة السريعة)
    app.run_polling()
    
    # الطريقة 2: Webhook (للإنتاج)
    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=int(os.environ.get("PORT", 8443)),
    #     url_path=TOKEN,
    #     webhook_url=f"https://YOUR_RAILWAY_URL.up.railway.app/{TOKEN}"
    # )
