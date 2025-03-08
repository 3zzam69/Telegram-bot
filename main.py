import re
import json
from datetime import datetime
from telegram import Update, InputFile, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

# التوكن الخاص ببوتك الحالي
TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
# التوكن الخاص ببوت الاستقبال
RECEIVER_BOT_TOKEN = "1724071074:AAHY4HlO6P6c2zrgJVtOwj30Iz0xgwhFoGU"
# معرف الدردشة الخاص ببوت الاستقبال
RECEIVER_CHAT_ID = "@p8q_bot"

# قاعدة بيانات بسيطة لحفظ المعلومات
user_data = {}

# الحالات للمحادثة
ASK_NAME, ASK_DAY, ASK_MONTH, ASK_YEAR, CONFIRM_DOB = range(5)

# وظيفة البداية
async def start(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    if chat_id in user_data:
        await update.message.reply_text(f'مرحبًا بك مرة أخرى، {user_data[chat_id]["name"]}!')
        return ConversationHandler.END
    else:
        await update.message.reply_text('مرحبًا! من فضلك أدخل اسمك الثلاثي باللغة العربية:')
        return ASK_NAME

# وظيفة التعامل مع الأسماء
async def handle_name(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    name = update.message.text

    # التحقق من أن الاسم يحتوي على حروف عربية فقط ويتكون من ثلاث كلمات كل واحدة تحتوي على حرفين على الأقل
    if re.match(r'^[\u0600-\u06FF\s]+$', name) and len(name.split()) == 3 and all(len(part) > 1 for part in name.split()):
        context.user_data['name'] = name
        keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 32)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('من فضلك اختر يوم ميلادك من القائمة:', reply_markup=reply_markup)
        return ASK_DAY
    else:
        await update.message.reply_text('الاسم يجب أن يكون ثلاثيًا وباللغة العربية فقط وكل كلمة تحتوي على حرفين على الأقل. من فضلك أدخل اسمك الصحيح:')
        return ASK_NAME

# وظيفة التعامل مع اليوم
async def handle_day(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['day'] = query.data
    keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 13)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('من فضلك اختر شهر ميلادك من القائمة:', reply_markup=reply_markup)
    return ASK_MONTH

# وظيفة التعامل مع الشهر
async def handle_month(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['month'] = query.data
    keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(datetime.now().year - 100, datetime.now().year)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('من فضلك اختر سنة ميلادك من القائمة:', reply_markup=reply_markup)
    return ASK_YEAR

# وظيفة التعامل مع السنة
async def handle_year(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['year'] = query.data
    dob = f"{context.user_data['year']}-{context.user_data['month']}-{context.user_data['day']}"
    await query.edit_message_text(f'هل هذا هو تاريخ ميلادك؟ {dob}', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("نعم", callback_data="confirm_dob")],
        [InlineKeyboardButton("تعديل", callback_data="edit_dob")]
    ]))
    return CONFIRM_DOB

# وظيفة تأكيد أو تعديل تاريخ الميلاد
async def confirm_dob(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_dob":
        chat_id = query.message.chat_id
        dob = f"{context.user_data['year']}-{context.user_data['month']}-{context.user_data['day']}"
        dob_datetime = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.now() - dob_datetime).days // 365
        if 5 <= age <= 100:
            user_data[chat_id] = {'name': context.user_data['name'], 'dob': dob}
            await query.edit_message_text(f'تم حفظ بياناتك بنجاح، {context.user_data["name"]}!')
            save_user_data()
            await send_file_to_receiver_bot()
            return ConversationHandler.END
        else:
            await query.edit_message_text('العمر يجب أن يكون بين 5 و 100 سنة. من فضلك أدخل تاريخ ميلاد صحيح:')
            return ASK_DAY
    else:
        await query.edit_message_text('من فضلك اختر يوم ميلادك من القائمة:')
        keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 32)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('من فضلك اختر يوم ميلادك من القائمة:', reply_markup=reply_markup)
        return ASK_DAY

# وظيفة حفظ البيانات في ملف
def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)

# وظيفة رفع الملف إلى بوت الاستقبال
async def send_file_to_receiver_bot():
    receiver_bot = Application.builder().token(RECEIVER_BOT_TOKEN).build()
    try:
        with open('user_data.json', 'rb') as file:
            input_file = InputFile(file, filename='user_data.json')
            await receiver_bot.bot.send_document(chat_id=RECEIVER_CHAT_ID, document=input_file)
    except Exception as e:
        print(f"Error sending file: {e}")

# إنشاء التطبيق
app = Application.builder().token(TOKEN).build()

# إعداد المحادثة
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
        ASK_DAY: [CallbackQueryHandler(handle_day)],
        ASK_MONTH: [CallbackQueryHandler(handle_month)],
        ASK_YEAR: [CallbackQueryHandler(handle_year)],
        CONFIRM_DOB: [CallbackQueryHandler(confirm_dob)]
    },
    fallbacks=[]
)

app.add_handler(conv_handler)

if __name__ == '__main__':
    app.run_polling()
