import os import time import threading from flask import Flask from telegram import Update, Bot from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv("BOT_TOKEN") PORT = int(os.getenv("PORT", 8080))

bot = Bot(token=TOKEN) updater = Updater(token=TOKEN, use_context=True) dp = updater.dispatcher

user_reminders = {}

def send_reminder(user_id): while user_id in user_reminders: time.sleep(1800)  # 30 minutes if user_id in user_reminders and user_reminders[user_id]['mode'] == 'active': bot.send_message(user_id, "Reminder: Change your email!") else: break

def start(update: Update, context: CallbackContext): user_id = update.message.chat_id if user_id in user_reminders: update.message.reply_text("You're already subscribed to reminders!") else: next_change = time.time() + 6 * 24 * 60 * 60 user_reminders[user_id] = {'mode': 'active', 'next_change': next_change} threading.Thread(target=send_reminder, args=(user_id,)).start() update.message.reply_text("Welcome! You'll get reminders every 30 minutes until you confirm.")

def check(update: Update, context: CallbackContext): user_id = update.message.chat_id if user_id in user_reminders: next_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_reminders[user_id]['next_change'])) update.message.reply_text(f"Your next email change is scheduled on: {next_time}") else: update.message.reply_text("You're not subscribed to reminders.")

def done(update: Update, context: CallbackContext): user_id = update.message.chat_id if user_id in user_reminders: next_change = time.time() + 6 * 24 * 60 * 60 user_reminders[user_id] = {'mode': 'inactive', 'next_change': next_change} next_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_change)) update.message.reply_text(f"Thanks! Your next email change is scheduled on: {next_time}") else: update.message.reply_text("You're not subscribed to reminders.")

dp.add_handler(CommandHandler("start", start)) dp.add_handler(CommandHandler("check", check)) dp.add_handler(CommandHandler("done", done))

app = Flask(name)

@app.route('/') def home(): return "Bot is running!"

def run_flask(): app.run(host='0.0.0.0', port=PORT)

def run_telegram(): updater.start_polling() updater.idle()

if name == "main": threading.Thread(target=run_flask).start() run_telegram()

