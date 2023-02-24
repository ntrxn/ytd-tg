import logging
import os
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from pytube import YouTube

# Logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a YouTube downloader bot. Just send me the link of the YouTube video you want to download and I will send it to you.")

# function to handle messages with YouTube link
def download(update, context):
    chat_id = update.effective_chat.id
    link = update.message.text
    try:
        video = YouTube(link)
        stream = video.streams.get_highest_resolution()
        stream.download()
        context.bot.send_video(chat_id=chat_id, video=open(f'{video.title}.mp4', 'rb'), supports_streaming=True)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="Sorry, an error occurred while downloading the video.")

# Replace TELEGRAM_API_TOKEN with your bot token
def main():
    updater = Updater(token=os.environ.get('TELEGRAM_API_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    download_handler = MessageHandler(Filters.regex(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'), download)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
