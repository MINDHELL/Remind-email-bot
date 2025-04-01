import asyncio
import datetime
import os
from telegram import Bot, ParseMode, Update
from telegram.ext import CommandHandler, Updater, CallbackContext
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Ensure your token is in a .env file
CHAT_ID = os.getenv("CHAT_ID")  # Optional: If you have a specific chat ID

# Initialize the bot and FastAPI app
app = FastAPI()
reminder_times = {}

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    welcome_text = "<b>✨ Welcome! ✨</b>\n\n🚀 I will remind you to change your Telegram email every 7 days! 🔄\n\nUse <b>/done</b> ✅ when you've changed it!"
    update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)

# Define the done command
def done(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    next_reminder = datetime.datetime.now() + datetime.timedelta(days=6, hours=23, minutes=30)
    reminder_times[user_id] = next_reminder
    response_text = f"✅ <b>Thanks!</b> Your next reminder is on: 📅 <b>{next_reminder.strftime('%d %B %Y, %H:%M:%S')}</b> ⏳"
    update.message.reply_text(response_text, parse_mode=ParseMode.HTML)

# Function to send reminders
async def send_reminder(updater: Updater) -> None:
    while True:
        now = datetime.datetime.now()
        for user_id, reminder_time in reminder_times.items():
            if reminder_time.date() == now.date():
                time_left = (reminder_time - now).total_seconds()
                if time_left <= 0:
                    reminder_message = "⏳ <b>Reminder:</b> Don't forget to change your Telegram email today! 📩\n\nUse <b>/done</b> ✅ after updating it!"
                    updater.bot.send_message(user_id, reminder_message, parse_mode=ParseMode.HTML)
                    reminder_times[user_id] = now + datetime.timedelta(minutes=30)
        await asyncio.sleep(1800)  # Check every 30 minutes

# FastAPI route to check bot status
@app.get("/")
def read_root():
    return {"status": "🚀 Bot is running smoothly!"}

# Set up the Updater and Dispatcher
def main():
    """Start the bot, set up the command handlers, and start polling for updates."""
    # Create the Updater and pass in your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register command handlers
    dispatcher = updater.dispatcher

    # Register handlers for the /start and /done commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("done", done))

    # Start the bot with polling
    updater.start_polling()

    # Start sending reminders in the background
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminder(updater))

    # Keep the bot running until manually stopped
    updater.idle()

if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=80)
