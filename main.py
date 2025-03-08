import re
import json
from datetime import datetime
from telegram import Update, InputFile, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# التوكن الخاص ببوتك الحالي
TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
# التوكن الخاص ببوت الاستقبال
RECEIVER_BOT_TOKEN = "1724071074:AAHY4HlO6P6c2zrgJVtOwj30Iz0xgwhFoGU"
# معرف الدردشة الخاص ببوت الاستقبال
RECEIVER_CHAT_ID = "@p8q_bot"

# قاعدة بيانات بسيطة لحفظ المعلومات
user_data = {}

# الحالات للمحادثة
ASK_NAME, ASK_DOB, CONFIRM_DOB = range(3)

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
        keyboard = [[str(i)] for i in range(1, 32)]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text('من فضلك اختر يوم ميلادك من القائمة:', reply_markup=reply_markup)
        return ASK_DOB
    else:
        await update.message.reply_text('الاسم يجب أن يكون ثلاثيًا وباللغة العربية فقط وكل كلمة تحتوي على حرفين على الأقل. من فضلك أدخل اسمك الصحيح:')
        return ASK_NAME

# وظيفة التعامل مع اليوم
async def handle_day(update: Update, context: CallbackContext) -> int:
    day = update.message.text
    if day.isdigit() and 1 <= int(day) <= 31:
        context.user_data['day'] = day
        keyboard = [[str(i)] for i in range(1, 13)]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text('من فضلك اختر شهر ميلادك من القائمة:', reply_markup=reply_markup)
        return CONFIRM_DOB
    else:
        await update.message.reply_text('اليوم غير صالح. من فضلك اختر يومًا صحيحًا من القائمة:')
        return ASK_DOB

# وظيفة التعامل مع الشهر
async def handle_month(update: Update, context: CallbackContext) -> int:
    month = update.message.text
    if month.isdigit() and 1 <= int(month) <= 12:
        context.user_data['month'] = month
        keyboard = [[str(i)] for i in range(datetime.now().year - 100, datetime.now().year)]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text('من فضلك اختر سنة ميلادك من القائمة:', reply_markup=reply_markup)
        return CONFIRM_DOB
    else:
        await update.message.reply_text('الشهر غير صالح. من فضلك اختر شهرًا صحيحًا من القائمة:')
        return ASK_DOB

# وظيفة التعامل مع السنة
async def handle_year(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    year = update.message.text
    if year.isdigit() and datetime.now().year - 100 <= int(year) <= datetime.now().year:
        context.user_data['year'] = year
        dob = f"{context.user_data['year']}-{context.user_data['month']}-{context.user_data['day']}"
        dob_datetime = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.now() - dob_datetime).days // 365
        if 5 <= age <= 100:
            user_data[chat_id] = {'name': context.user_data['name'], 'dob': dob}
            await update.message.reply_text(f'تم حفظ بياناتك بنجاح، {context.user_data["name"]}!')
            save_user_data()
            await send_file_to_receiver_bot()
            return ConversationHandler.END
        else:
            await update.message.reply_text('العمر يجب أن يكون بين 5 و 100 سنة. من فضلك أدخل تاريخ ميلاد صحيح:')
            return CONFIRM_DOB
    else:
        await update.message.reply_text('السنة غير صالحة. من فضلك اختر سنة صحيحة من القائمة:')
        return CONFIRM_DOB

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
        ASK_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day)],
        CONFIRM_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_month)]
    },
    fallbacks=[]
)

app.add_handler(conv_handler)

if __name__ == '__main__':
    app.run_polling()
