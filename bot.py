import asyncio
import datetime
import os
from telegram import Bot, Update
from telegram.constants import ParseMode
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Ensure your token is in a .env file
CHAT_ID = os.getenv("CHAT_ID")  # Optional: If you have a specific chat ID

bot = Bot(token=TOKEN)
app = FastAPI()

reminder_times = {}

# Handler for /start command
async def start_command(update: Update, context):
    welcome_text = "<b>✨ Welcome! ✨</b>\n\n🚀 I will remind you to change your Telegram email every 7 days! 🔄\n\nUse <b>/done</b> ✅ when you've changed it!"
    await update.message.reply(welcome_text, parse_mode=ParseMode.HTML)

# Handler for /done command
async def done_command(update: Update, context):
    user_id = update.message.from_user.id
    next_reminder = datetime.datetime.now() + datetime.timedelta(days=6, hours=23, minutes=30)
    reminder_times[user_id] = next_reminder
    response_text = f"✅ <b>Thanks!</b> Your next reminder is on: 📅 <b>{next_reminder.strftime('%d %B %Y, %H:%M:%S')}</b> ⏳"
    await update.message.reply(response_text, parse_mode=ParseMode.HTML)

# Function to send reminder
async def send_reminder():
    while True:
        now = datetime.datetime.now()
        for user_id, reminder_time in reminder_times.items():
            if reminder_time.date() == now.date():
                time_left = (reminder_time - now).total_seconds()
                if time_left <= 0:
                    reminder_message = "⏳ <b>Reminder:</b> Don't forget to change your Telegram email today! 📩\n\nUse <b>/done</b> ✅ after updating it!"
                    await bot.send_message(user_id, reminder_message, parse_mode=ParseMode.HTML)
                    reminder_times[user_id] = now + datetime.timedelta(minutes=30)
        await asyncio.sleep(1800)  # Check every 30 minutes

@app.get("/")
def read_root():
    return {"status": "🚀 Bot is running smoothly!"}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminder())
    uvicorn.run(app, host="0.0.0.0", port=8080)
