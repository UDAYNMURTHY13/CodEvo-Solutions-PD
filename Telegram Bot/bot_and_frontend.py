from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, render_template, request
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Telegram bot token
TELEGRAM_TOKEN = '7287368386:AAFjnOYK6MbB8nA-LzTdVdSugoXSpO2li3o'

# Create a Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

# Create a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Flask Route for Frontend
@app.route('/')
def home():
    return render_template('index.html')

# Flask Route for sending message through the bot
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    
    try:
        # Use a fixed chat_id (replace with actual recipient's chat ID)
        chat_id = 'YOUR_FIXED_CHAT_ID'

        # Use asyncio to send a message
        asyncio.run_coroutine_threadsafe(bot.send_message(chat_id=chat_id, text=message), loop)
        return 'Message sent successfully!'
    except Exception as e:
        return f"Error: {e}"

# Function to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am your bot.')

# Function to handle messages
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f'You said: {text}')

# Initialize Telegram bot
async def telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler('start', start))

    # Message handling
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Initialize the application
    await application.initialize()

    # Start polling
    await application.start_polling()
    await application.updater.idle()

# Run both Flask app and Telegram bot
if __name__ == '__main__':
    from threading import Thread

    # Start the Telegram bot in a separate thread
    bot_thread = Thread(target=lambda: loop.run_until_complete(telegram_bot()))
    bot_thread.start()

    # Start Flask app
    app.run(debug=True)
