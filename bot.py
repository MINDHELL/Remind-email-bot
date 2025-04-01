import asyncio
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Set this in your Koyeb environment variables

# Reminder Configuration
REMINDER_INTERVAL_DAYS = 6
NEXT_CHANGE_DATE = datetime.now() + timedelta(days=REMINDER_INTERVAL_DAYS)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def send_reminder():
    """ Sends a reminder message every 6 days """
    global NEXT_CHANGE_DATE
    while True:
        await bot.send_message(CHAT_ID, f"🔔 Reminder: Change your Telegram login email today!\nNext change: {NEXT_CHANGE_DATE.strftime('%Y-%m-%d')}")
        NEXT_CHANGE_DATE += timedelta(days=REMINDER_INTERVAL_DAYS)
        await asyncio.sleep(REMINDER_INTERVAL_DAYS * 24 * 60 * 60)  # Wait 6 days

@dp.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    """ Sends a welcome message when the user sends /start """
    await message.answer("👋 Welcome! I will remind you to change your Telegram login email every 6 days.\n\nUse /next to check the next change date.")

@dp.message(lambda message: message.text == "/next")
async def next_change(message: types.Message):
    """ Sends the next email change date when the user sends /next """
    time_left = NEXT_CHANGE_DATE - datetime.now()
    days_left = time_left.days
    await message.answer(f"📅 Next email change: {NEXT_CHANGE_DATE.strftime('%Y-%m-%d')}\n⏳ Time left: {days_left} days")

async def main():
    """ Starts the bot and the reminder loop """
    asyncio.create_task(send_reminder())  # Run reminder loop in the background
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
