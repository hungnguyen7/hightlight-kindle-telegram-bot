from dotenv import load_dotenv
import telebot
import os

# Load environment variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    return



bot.infinity_polling()
