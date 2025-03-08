from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# التوكن الخاص بك
TOKEN = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Welcome to my bot.')

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    app.run_polling()
