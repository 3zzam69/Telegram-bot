from pyrogram import Client
import config

bot = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@bot.on_message()
def hello(client, message):
    message.reply_text("مرحبًا، البوت يعمل بنجاح!")

bot.run()
