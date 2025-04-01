import asyncio
import datetime
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ParseMode
from aiogram import Application
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Replace with actual chat ID if needed

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
app = FastAPI()

reminder_times = {}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    welcome_text = "<b>✨ Welcome! ✨</b>\n\n🚀 I will remind you to change your Telegram email every 7 days! 🔄\n\nUse <b>/done</b> ✅ when you've changed it!"
    await message.reply(welcome_text)

@dp.message_handler(commands=['done'])
async def done_command(message: types.Message):
    user_id = message.from_user.id
    next_reminder = datetime.datetime.now() + datetime.timedelta(days=6, hours=23, minutes=30)
    reminder_times[user_id] = next_reminder
    response_text = f"✅ <b>Thanks!</b> Your next reminder is on: 📅 <b>{next_reminder.strftime('%d %B %Y, %H:%M:%S')}</b> ⏳"
    await message.reply(response_text)

async def send_reminder():
    while True:
        now = datetime.datetime.now()
        for user_id, reminder_time in reminder_times.items():
            if reminder_time.date() == now.date():
                time_left = (reminder_time - now).total_seconds()
                if time_left <= 0:
                    reminder_message = "⏳ <b>Reminder:</b> Don't forget to change your Telegram email today! 📩\n\nUse <b>/done</b> ✅ after updating it!"
                    await bot.send_message(user_id, reminder_message)
                    reminder_times[user_id] = now + datetime.timedelta(minutes=30)
        await asyncio.sleep(1800)  # Check every 30 minutes

@app.get("/")
def read_root():
    return {"status": "🚀 Bot is running smoothly!"}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminder())
    app.run_polling()
