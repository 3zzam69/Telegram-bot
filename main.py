import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, ContextTypes

# تحميل المتغيرات البيئية
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
RECEIVER_BOT_TOKEN = os.getenv("RECEIVER_BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# إعدادات السجل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ثوابت المحادثة
SELECT_MONTH, SELECT_YEAR = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال رسالة ترحيب وزر اختيار شهر الميلاد"""
    keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i))] for i in range(1, 13)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر شهر ميلادك:", reply_markup=reply_markup)
    return SELECT_MONTH

async def handle_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عند اختيار الشهر، يعرض السنوات المتاحة"""
    query = update.callback_query
    await query.answer()
    
    # تخزين الشهر المختار
    context.user_data["month"] = int(query.data)
    
    # عرض اختيار السنة
    return await show_year_selection(query, context)

async def show_year_selection(query, context):
    """عرض قائمة السنوات بشكل مناسب"""
    context.user_data["year_page"] = 2025  # أحدث سنة متاحة
    return await update_year_selection(query, context)

async def update_year_selection(query, context):
    """تحديث عرض السنوات حسب الصفحة"""
    year_page = context.user_data["year_page"]
    years = [year_page - i for i in range(5)]  # عرض 5 سنوات فقط

    keyboard = [[InlineKeyboardButton(str(year), callback_data=str(year))] for year in years]
    keyboard.append([
        InlineKeyboardButton("⬅️ السابق", callback_data="prev_years"),
        InlineKeyboardButton("التالي ➡️", callback_data="next_years"),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("اختر سنة ميلادك:", reply_markup=reply_markup)
    return SELECT_YEAR

async def handle_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حفظ سنة الميلاد وإنهاء المحادثة"""
    query = update.callback_query
    await query.answer()
    context.user_data["year"] = int(query.data)

    month = context.user_data["month"]
    year = context.user_data["year"]

    await query.edit_message_text(f"تم اختيار تاريخ الميلاد: {month}/{year}")
    return ConversationHandler.END

async def navigate_years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التنقل بين السنوات عند اختيار تاريخ الميلاد"""
    query = update.callback_query
    await query.answer()

    if query.data == "prev_years":
        context.user_data["year_page"] -= 5
    elif query.data == "next_years":
        context.user_data["year_page"] += 5

    return await update_year_selection(query, context)

def main():
    """تشغيل البوت"""
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_MONTH: [CallbackQueryHandler(handle_month)],
            SELECT_YEAR: [
                CallbackQueryHandler(handle_year, pattern=r"^\d+$"),
                CallbackQueryHandler(navigate_years, pattern="^(prev_years|next_years)$"),
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
