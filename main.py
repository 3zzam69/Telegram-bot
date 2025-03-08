import re
import json
from datetime import datetime
from telegram import Update, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

# التوكنات والمعرفات
TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"
RECEIVER_BOT_TOKEN = "1724071074:AAHY4HlO6P6c2zrgJVtOwj30Iz0xgwhFoGU"
RECEIVER_CHAT_ID = "@p8q_bot"

# تحميل البيانات المخزنة
try:
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    user_data = {}

# حالات المحادثة
ASK_NAME, ASK_DAY, ASK_MONTH, ASK_YEAR, CONFIRM_DOB = range(5)

async def start(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    if str(chat_id) in user_data:
        await update.message.reply_text(f'مرحبًا بك مرة أخرى، {user_data[str(chat_id)]["name"]}!')
        return ConversationHandler.END
    else:
        await update.message.reply_text('مرحبًا! أدخل اسمك الثلاثي باللغة العربية:')
        return ASK_NAME

async def handle_name(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    name = update.message.text.strip()

    if re.match(r'^[\u0600-\u06FF\s]+$', name) and len(name.split()) == 3 and all(len(part) > 1 for part in name.split()):
        context.user_data['name'] = name
        keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(j, j+6)] for j in range(1, 31, 6)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('اختر يوم ميلادك:', reply_markup=reply_markup)
        return ASK_DAY
    else:
        await update.message.reply_text('يجب إدخال اسم ثلاثي باللغة العربية، كل كلمة تحتوي على حرفين على الأقل:')
        return ASK_NAME

async def handle_day(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['day'] = query.data

    keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 7)],
                [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(7, 13)]]
    await query.edit_message_text('اختر شهر ميلادك:', reply_markup=InlineKeyboardMarkup(keyboard))
    return ASK_MONTH

async def handle_month(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['month'] = query.data

    context.user_data['year_page'] = datetime.now().year - 5  # آخر 5 سنوات
    return await show_year_selection(query)

async def show_year_selection(query):
    year_page = query.message.chat.id
    current_year = datetime.now().year
    years = [context.user_data['year_page'] - i for i in range(5)]
    
    keyboard = [[InlineKeyboardButton(str(year), callback_data=str(year)) for year in years],
                [InlineKeyboardButton("⬅️ السابق", callback_data="prev_year"), InlineKeyboardButton("التالي ➡️", callback_data="next_year")]]
    
    await query.edit_message_text('اختر سنة ميلادك:', reply_markup=InlineKeyboardMarkup(keyboard))
    return ASK_YEAR

async def handle_year(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "next_year":
        context.user_data['year_page'] -= 5
        return await show_year_selection(query)
    elif query.data == "prev_year":
        context.user_data['year_page'] += 5
        return await show_year_selection(query)

    context.user_data['year'] = query.data

    dob = f"{context.user_data['year']}-{context.user_data['month']}-{context.user_data['day']}"
    buttons = [
        [InlineKeyboardButton("✅ نعم", callback_data="confirm_dob")],
        [InlineKeyboardButton("🔄 تعديل", callback_data="edit_dob")]
    ]
    await query.edit_message_text(f'تاريخ ميلادك: {dob}. هل هذا صحيح؟', reply_markup=InlineKeyboardMarkup(buttons))
    return CONFIRM_DOB

async def confirm_dob(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_dob":
        chat_id = str(query.message.chat.id)
        dob = f"{context.user_data['year']}-{context.user_data['month']}-{context.user_data['day']}"
        dob_datetime = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.now() - dob_datetime).days // 365

        if 5 <= age <= 100:
            user_data[chat_id] = {'name': context.user_data['name'], 'dob': dob}
            save_user_data()
            await query.edit_message_text(f'✅ تم حفظ بياناتك بنجاح، {context.user_data["name"]}!')
            await send_file_to_receiver_bot()
            return ConversationHandler.END
        else:
            await query.edit_message_text('⚠️ يجب أن يكون عمرك بين 5 و 100 سنة. أدخل تاريخ ميلاد صحيح:')
            return ASK_DAY
    else:
        return await restart_dob_selection(query)

async def restart_dob_selection(query):
    keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 7)],
                [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(7, 13)]]
    await query.edit_message_text('اختر شهر ميلادك مرة أخرى:', reply_markup=InlineKeyboardMarkup(keyboard))
    return ASK_MONTH

def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)

async def send_file_to_receiver_bot():
    try:
        receiver_bot = Application.builder().token(RECEIVER_BOT_TOKEN).build()
        with open('user_data.json', 'rb') as file:
            input_file = InputFile(file, filename='user_data.json')
            await receiver_bot.bot.send_document(chat_id=RECEIVER_CHAT_ID, document=input_file)
    except Exception as e:
        print(f"❌ خطأ أثناء إرسال الملف: {e}")

app = Application.builder().token(TOKEN).build()

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
