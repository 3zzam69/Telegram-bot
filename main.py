from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
import time

API_ID = 27155532  # �1�4�1�7 API_ID �1�1�1�0�1�9
API_HASH = "7809990459:AAHnk6DHKeox2iyLA9mOKge4d02rW7O67n8"  # �1�4�1�7 API_HASH �1�1�1�0�1�9
BOT_TOKEN = "4b49a9b7bc41ad7f3c66d88a47f24ecc"  # �1�4�1�7 �1�2�1�2�1�7�1�0 �1�9�1�8�1�0�1�2�1�2 �1�1�1�0�1�9

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

CHANNEL_USERNAME = "Non_Arab"  # �1�4�1�7 �1�9�1�7�1�9�1�5 �1�9�1�8�1�6�1�0�1�9�1�1 �1�0�1�7�1�2�1�0 @

def is_user_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"�1�6�1�5�1�5 �1�5�1�3�1�0�1�9�1�3 �1�9�1�8�1�2�1�5�1�6�1�6 �1�9�1�0 �1�9�1�8�1�9�1�2�1�2�1�9�1�9�1�7: {e}")
        return False

@bot.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id

    while not is_user_subscribed(user_id):
        message.reply_text(f"�9�2 **�1�4�1�4�1�0 �1�7�1�8�1�4�1�7 �1�9�1�8�1�9�1�2�1�2�1�9�1�9�1�7 �1�5�1�4 �1�9�1�8�1�6�1�0�1�9�1�1 �1�8�1�9�1�1�1�2�1�6�1�7�1�9�1�9 �1�9�1�8�1�0�1�2�1�2!**\n"
                           f"�9�7 [�1�9�1�4�1�8�1�5 �1�1�1�0�1�9 �1�8�1�8�1�9�1�2�1�2�1�9�1�9�1�7](https://t.me/{CHANNEL_USERNAME}) �1�3�1�9 �1�5�1�9�1�1�1�8 /start �1�9�1�9�1�1 �1�5�1�6�1�9�1�3.",
                           disable_web_page_preview=True)
        
        time.sleep(10)  # �1�9�1�0�1�2�1�6�1�9�1�9 10 �1�3�1�2�1�9�1�0�1�7 �1�6�1�0�1�8 �1�7�1�7�1�9�1�7�1�1 �1�9�1�8�1�2�1�5�1�6�1�6

    message.reply_text("�7�3 **�1�5�1�1�1�8�1�9 �1�0�1�7! �1�2�1�9 �1�9�1�8�1�2�1�5�1�6�1�6 �1�9�1�0 �1�9�1�2�1�2�1�9�1�9�1�7�1�7 �1�0�1�0�1�4�1�9�1�5. �1�4�1�9�1�7�1�0�1�7 �1�9�1�8�1�4�1�0 �1�9�1�1�1�2�1�6�1�7�1�9�1�9 �1�9�1�8�1�0�1�2�1�2.**")

bot.run()