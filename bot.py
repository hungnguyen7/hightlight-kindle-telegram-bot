from dotenv import load_dotenv
import telebot
import os
import schedule
from utils.highlight_handler import process_and_store_highlights, load_random_highlight
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Store schedules dynamically with unique chat_ids
schedules = {}


# Command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Hello! I send random Kindle highlights. Use /import to upload highlights.")


# Command to show help message
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /import - Import highlights
    /highlight - Show random highlight
    /schedule - Set schedule time
    /unschedule - Delete scheduled message
    """)


# Command to show random highlight
@bot.message_handler(commands=['highlight'])
def send_random_highlight(message):
    try:
        highlights = load_random_highlight()
        bot.reply_to(message, format_highlight(
            highlights), parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


@bot.message_handler(commands=['import'])
def import_highlights(message):
    bot.send_message(message.chat.id, "Please upload the highlights.txt file.")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.mime_type == 'text/plain':
        try:
            file_info = bot.get_file(message.document.file_id)
            with open("highlights.txt", 'wb') as new_file:
                new_file.write(bot.download_file(file_info.file_path))
            process_and_store_highlights()
            bot.reply_to(message, "Highlights imported successfully!")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Please upload a valid .txt file.")


# Command to set schedule time
@bot.message_handler(commands=['schedule'])
def schedule_time_selection(message):
    markup = InlineKeyboardMarkup()

    # Options for scheduling time (in minutes)
    for i in [1, 5, 10, 30, 60, 120]:  # Add more intervals if needed
        markup.add(InlineKeyboardButton(
            f"{i} minutes", callback_data=f"schedule_{i}"))

    bot.send_message(
        message.chat.id, "Choose the time interval for sending a random highlight:", reply_markup=markup)


# Handle callback for scheduling
@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule_'))
def handle_schedule_callback(call):
    try:
        interval = int(call.data.split('_')[1])

        # Clear any existing schedules for this chat
        if call.message.chat.id in schedules:
            schedule.clear(schedules[call.message.chat.id])

        # Schedule a new job
        job = schedule.every(interval).minutes.do(
            send_scheduled_highlight, call.message)
        schedules[call.message.chat.id] = job

        bot.send_message(call.message.chat.id, f"Scheduled to send a random highlight every {interval} minutes.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error scheduling: {e}")


# Command to delete scheduled message
@bot.message_handler(commands=['unschedule'])
def unschedule(message):
    if message.chat.id in schedules:
        schedule.cancel_job(schedules[message.chat.id])
        del schedules[message.chat.id]
        bot.send_message(message.chat.id, "Your schedule has been deleted.")
    else:
        bot.send_message(message.chat.id, "No schedule found to delete.")


# Function to send scheduled highlights
def send_scheduled_highlight(message):
    try:
        highlights = load_random_highlight()
        bot.send_message(message.chat.id, format_highlight(
            highlights), parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


# Helper function to format the highlights
def format_highlight(highlights):
    if highlights is None:
        return "No highlights found. Please import highlights first using /import."

    return (f"📚 *{highlights['book_title']}*"
            f"\n📍 Location: {highlights['location']}"
            f"\n🕒 Added on: {highlights['timestamp']}"
            f"\n\n{highlights['text']}")


# Scheduler loop
def run_scheduler():
    while True:
        schedule.run_pending()


# Run bot and scheduler
if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    print("Bot is running...")
    bot.infinity_polling()
