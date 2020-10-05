from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, PicklePersistence
from settings import TELEGRAM_BOT_TOKEN, MAX_AGE_IN_SECONDS
from datetime import datetime, timezone
from threading import Thread
from time import sleep

bot = Bot(TELEGRAM_BOT_TOKEN)


def handle_new_channel_posts(update, context):
    # a function to listen to new messages in channel
    message_id = update.channel_post.message_id
    timestamp = update.channel_post.date

    # a function to store message_id and timestamp
    context.chat_data[message_id] = {"timestamp": timestamp, "deleted": False, "message_id": message_id}


# a function to calculate message age
def calculate_message_age():
    while True:
        for key, value in dp.chat_data.items():
            for message_id, message_data in value.items():
                if message_data.get("deleted"):
                    continue
                age = (datetime.now(tz=timezone.utc) - message_data['timestamp']).total_seconds()
                if age > MAX_AGE_IN_SECONDS:
                    # a function to delete the old message
                    try:
                        bot.delete_message(chat_id=key, message_id=message_id)
                    except Exception:
                        pass
                    message_data["deleted"] = True
                    sleep(0.10)
        sleep(1)


my_persistence = PicklePersistence(filename='my_bot_data')
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True, persistence=my_persistence)
dp = updater.dispatcher
updater.dispatcher.add_handler(MessageHandler(Filters.update.channel_post, handle_new_channel_posts))

Thread(target=calculate_message_age).start()

updater.start_polling()
updater.idle()
