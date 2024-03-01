# Importing necessary libraries
import os
import threading
import telebot
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Initializing Telegram bot with API token
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))


# Function to send message to specified Telegram ID
def send_message(message):
    """
    Sends a message to the specified Telegram ID.

    Args:
        message (str): The message to be sent.

    Note:
        The message will be sent to the Telegram ID specified in the environment variable TELEGRAM_ID.
    """
    if message:  # Checking if the message is not empty
        bot.send_message(os.environ.get("TELEGRAM_ID"), message)


# Function to run the Telegram bot
def run_bot():
    """
    Runs the Telegram bot.

    This function starts the Telegram bot in a separate thread for continuous polling.
    """
    print("Telegram bot running!")
    # Creating a new thread for bot polling
    thread = threading.Thread(target=bot.infinity_polling)
    thread.start()
