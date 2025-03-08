from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.environ.get("7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8")  # سيأخذ التوكن من إعدادات Railway

# ─── تفسير الأحلام (بيانات وهمية للاختبار) ───
dream_db = {
    "ثعبان": "رؤية الثعبان تدل على عدو ماكر",
    "مطر": "الخير الوفير والبركة",
    "سفر": "تغيير إيجابي قادم في حياتك",
}

# ─── رد على أمر /start ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"مرحبًا {user.first_name}! أرسل لي حلمك وسأفسره.")

# ─── تفسير الأحلام ───
async def interpret_dream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dream = update.message.text.lower()
    interpretation = dream_db.get(dream, "التفسير غير متوفر حالياً. جرب كلمات أخرى.")
    await update.message.reply_text(f"تفسير حلم '{dream}':\n{interpretation}")

# ─── تشغيل البوت ───
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    
    # الأوامر
    app.add_handler(CommandHandler("start", start))
    
    # معالجة الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interpret_dream))
    
    # التشغيل
    app.run_polling()
