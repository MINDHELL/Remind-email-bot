import asyncio
import datetime
import os
from telegram import Bot, ParseMode, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import logging

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Ensure your token is in a .env file
CHAT_ID = os.getenv("CHAT_ID")  # Optional: If you have a specific chat ID

bot = Bot(token=TOKEN)
app = FastAPI()

reminder_times = {}

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Command: /start
async def start_command(update: Update, context):
    welcome_text = "<b>✨ Welcome! ✨</b>\n\n🚀 I will remind you to change your Telegram email every 7 days! 🔄\n\nUse <b>/done</b> ✅ when you've changed it!"
    try:
        await update.message.reply(welcome_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Error in /start command: {e}")
        await update.message.reply("Something went wrong! Please try again later.")

# Command: /done
async def done_command(update: Update, context):
    user_id = update.message.from_user.id
    try:
        next_reminder = datetime.datetime.now() + datetime.timedelta(days=6, hours=23, minutes=30)
        reminder_times[user_id] = next_reminder
        response_text = f"✅ <b>Thanks!</b> Your next reminder is on: 📅 <b>{next_reminder.strftime('%d %B %Y, %H:%M:%S')}</b> ⏳"
        await update.message.reply(response_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Error in /done command: {e}")
        await update.message.reply("Something went wrong! Please try again later.")

# Send reminders function
async def send_reminder():
    while True:
        now = datetime.datetime.now()
        for user_id, reminder_time in reminder_times.items():
            try:
                if reminder_time.date() == now.date():
                    time_left = (reminder_time - now).total_seconds()
                    if time_left <= 0:
                        reminder_message = "⏳ <b>Reminder:</b> Don't forget to change your Telegram email today! 📩\n\nUse <b>/done</b> ✅ after updating it!"
                        await bot.send_message(user_id, reminder_message, parse_mode=ParseMode.HTML)
                        reminder_times[user_id] = now + datetime.timedelta(minutes=30)
            except Exception as e:
                logging.error(f"Error in send_reminder: {e}")
        await asyncio.sleep(1800)  # Check every 30 minutes

# Main entry point for the bot
def main():
    # Initialize the Updater and Dispatcher for handling commands
    try:
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Command handlers
        start_handler = CommandHandler('start', start_command)
        done_handler = CommandHandler('done', done_command)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(done_handler)

        # Start polling for updates
        updater.start_polling()
        logging.info("Bot started successfully!")

    except Exception as e:
        logging.error(f"Error in bot setup: {e}")

if __name__ == "__main__":
    # Run the FastAPI app in the background and start the bot
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminder())  # Start the reminder task

    # Run the FastAPI app using Uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logging.error(f"Error starting FastAPI app: {e}")
        print(f"Error starting FastAPI app: {e}")

    # Run the bot in the main thread
    main()
