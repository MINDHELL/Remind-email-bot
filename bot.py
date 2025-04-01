import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Bot Configuration
TOKEN = os.getenv("7920072240:AAFwCTASvGi65oRkHRBm1275Mte8p3Q6p0E")
CHAT_ID = os.getenv("-1002652118002")  # Replace with your Telegram ID in environment variables
REMINDER_INTERVAL_DAYS = 6
NEXT_CHANGE_DATE = datetime.now() + timedelta(days=REMINDER_INTERVAL_DAYS)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def send_reminder():
    global NEXT_CHANGE_DATE
    while True:
        await bot.send_message(CHAT_ID, f"Reminder: Change your Telegram login email today! Next change on {NEXT_CHANGE_DATE.strftime('%Y-%m-%d')}")
        NEXT_CHANGE_DATE += timedelta(days=REMINDER_INTERVAL_DAYS)
        await asyncio.sleep(REMINDER_INTERVAL_DAYS * 24 * 60 * 60)  # Wait 6 days

@dp.message_handler(commands=["next"])
async def next_change(message: types.Message):
    time_left = NEXT_CHANGE_DATE - datetime.now()
    days_left = time_left.days
    await message.reply(f"Next email change: {NEXT_CHANGE_DATE.strftime('%Y-%m-%d')}\nTime left: {days_left} days")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminder())
    executor.start_polling(dp, skip_updates=True)
