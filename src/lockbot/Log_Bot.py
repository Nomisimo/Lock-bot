import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import asyncio
from datetime import datetime, timedelta


# from config import TELEGRAM_API_KEY, CHAT_ID, LOCK_ID, NUKI_API_KEY, log

import config
from config import log
from lock_control import lock_command, unlock_command, validate_chat_id, get_lock_logs, get_battery_status

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

# Function to format the timestamp with timezone adjustment
def format_timestamp(log_date, timezone_offset=1):
    try:
        # Parse the ISO date and adjust for timezone
        timestamp = datetime.fromisoformat(log_date.replace("Z", ""))
        timestamp += timedelta(hours=timezone_offset)
        return timestamp.strftime('%H:%M Uhr %d.%m.%y')
    except ValueError:
        return "Unknown Date"
    
# Initialize last known action
last_known_action = None

# Define allowed chat IDs
# ALLOWED_CHAT_IDS = {CHAT_ID}  # Use a set for efficient membership checking

# Function to escape markdown characters
def escape_markdown(text):
    return text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('[', '\\[').replace(']', '\\]')


async def send_status_update(context: CallbackContext):
    logs = await get_lock_logs()
    if not logs:
        log("No logs fetched, skipping status update.", 'lock_status')
        return

    latest_log = logs[0]
    lock_action = latest_log.get('action', None)
    user_name = latest_log.get('name', None)
    log_date = latest_log.get('date', '')

    if lock_action is None or user_name is None:
        log("No action or name found in the log entry.", 'lock_status')
        return

    global last_known_action
    if lock_action == last_known_action:
        log(f"Lock action hasn't changed. Current action: {ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')}", 'lock_status')
        return

    last_known_action = lock_action
    action_desc = ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')

    # Use the updated timestamp formatter
    formatted_date = format_timestamp(log_date, timezone_offset=1)

    message = (f"*{escape_markdown(user_name)}* has *{escape_markdown(action_desc)}*\n"
               f"the Door🚪\n" 
               f"at *{escape_markdown(formatted_date)}*\n")

    CHAT_ID = config.get("telegram", "CHAT_ID")
    

    try:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        log(f"Message sent to chat {CHAT_ID}: {message}", 'lock_status')
    except Exception as e:
        log(f"Failed to send message to chat {CHAT_ID}: {e}", 'lock_status')



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
        log(f"Failed to send battery status to chat {update.effective_chat.id}: {e}", 'battery')

# Command to start the bot
@validate_chat_id
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your Nuki Lock Bot. I will keep you updated with the lock status.")

# Main function to start the bot and schedule jobs
def main():
    API_KEY = config.get("telegram", "API_KEY")
    
    application = Application.builder().token(API_KEY).build()

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
    log("Starting the bot...", 'general')
    application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Bot stopped manually.", 'general')
    except Exception as e:
        log(f"Unexpected error: {e}", 'general')
