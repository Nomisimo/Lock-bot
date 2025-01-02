import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import asyncio
from datetime import datetime
from config import TELEGRAM_API_KEY, CHAT_ID, LOCK_ID, NUKI_API_KEY, log_message
from lock_control import lock_command, unlock_command

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Action descriptions
ACTION_DESCRIPTIONS = {
    1: "Unlocked 🔓",
    2: "Locked 🔒",
    3: "Unlatched 🔑",
    4: "used Lock'n'Go 🔒💨",
    5: "used Lock'n'Go with Unlatch 🔒🔑💨",
    6: "Unknown Action 6 ❓",
    7: "Unknown Action 7 ❓",
}

# Initialize last known action
last_known_action = None

# Define allowed chat IDs
ALLOWED_CHAT_IDS = {CHAT_ID}  # Use a set for efficient membership checking

# Function to escape markdown characters
def escape_markdown(text):
    return text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('[', '\\[').replace(']', '\\]')

# Decorator for chat ID validation
def validate_chat_id(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_CHAT_IDS:
            log_message(f"Unauthorized access attempt from chat ID {chat_id}.", 'security')
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Function to get lock logs and process lock status
async def get_lock_logs():
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}/log?limit=2'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {NUKI_API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                log_message(f"Failed to fetch data from Nuki API. Status code: {response.status_code}", 'lock_status')
                return None
            data = response.json()
            log_message(f"Full response from Nuki API: {data}", 'lock_status')
            return data
    except Exception as e:
        log_message(f"Failed to fetch lock logs: {e}", 'lock_status')
        return None

# Function to send lock status update
async def send_status_update(context: CallbackContext):
    if CHAT_ID not in ALLOWED_CHAT_IDS:
        log_message(f"Chat ID {CHAT_ID} is not authorized to receive updates.", 'lock_status')
        return

    logs = await get_lock_logs()
    if not logs:
        log_message("No logs fetched, skipping status update.", 'lock_status')
        return

    latest_log = logs[0]
    lock_action = latest_log.get('action', None)
    user_name = latest_log.get('name', None)

    if lock_action is None or user_name is None:
        log_message("No action or name found in the log entry.", 'lock_status')
        return

    global last_known_action
    if lock_action == last_known_action:
        log_message(f"Lock action hasn't changed. Current action: {ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')}", 'lock_status')
        return

    last_known_action = lock_action
    action_desc = ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')
    log_date = latest_log.get('date', '')

    try:
        formatted_date = datetime.fromisoformat(log_date.replace("Z", "")).strftime('%H:%M Uhr %d.%m.%y')
    except ValueError:
        formatted_date = "Unknown Date"

    message = (f"*{escape_markdown(user_name)}* has *{escape_markdown(action_desc)}*\n"
               f"the Door🚪\n" 
               f"at *{escape_markdown(formatted_date)}*\n")

    try:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        log_message(f"Message sent to chat {CHAT_ID}: {message}", 'lock_status')
    except Exception as e:
        log_message(f"Failed to send message to chat {CHAT_ID}: {e}", 'lock_status')

# Function to get battery status
async def get_battery_status():
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {NUKI_API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                log_message(f"Failed to fetch battery data. Status code: {response.status_code}", 'battery')
                return None
            data = response.json()
            log_message(f"Full response from Nuki API: {data}", 'battery')
            return data
    except Exception as e:
        log_message(f"Failed to fetch battery data: {e}", 'battery')
        return None

# Function to send battery status
@validate_chat_id
async def battery_status(update: Update, context: CallbackContext):
    data = await get_battery_status()
    if not data:
        await update.message.reply_text("Could not fetch battery status from Nuki API.")
        return

    battery_charge = data.get('state', {}).get('batteryCharge', 'Unknown')
    battery_critical = data.get('state', {}).get('batteryCritical', False)
    keypad_battery_critical = data.get('state', {}).get('keypadBatteryCritical', False)
    doorsensor_battery_critical = data.get('state', {}).get('doorsensorBatteryCritical', False)

    battery_message = (f"*Battery Status*\n"
                       f"*Lock:* {battery_charge}%{' (Critical🪫)' if battery_critical else '🔋'}\n"
                       f"*Keypad:* {'Critical 🪫' if keypad_battery_critical else 'Normal 🔋'}\n"
                       f"*Door Sensor:* {'Critical 🪫' if doorsensor_battery_critical else 'Normal 🔋'}\n")

    try:
        await update.message.reply_text(battery_message, parse_mode='Markdown')
    except Exception as e:
        log_message(f"Failed to send battery status to chat {update.effective_chat.id}: {e}", 'battery')

# Command to start the bot
@validate_chat_id
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your Nuki Lock Bot. I will keep you updated with the lock status.")

# Main function to start the bot and schedule jobs
def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    application.add_handler(CommandHandler("battery", battery_status))

    # Scheduler setup for periodic lock status updates
    scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()})
    job = scheduler.add_job(send_status_update, 'interval', seconds=10, args=[application])
    scheduler.start()

    # Start the bot
    log_message("Starting the bot...", 'general')
    application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_message("Bot stopped manually.", 'general')
    except Exception as e:
        log_message(f"Unexpected error: {e}", 'general')
