import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import asyncio
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nuki API Configuration
LOCK_ID = 17968122341
Nuki_API_KEY = '748c83fab5c4b45224d45025555a31ff9d6b57dff9aa1765703916611c078a2536085b5474b68312'

# Telegram bot configuration
TELEGRAM_API_KEY = '7993283863:AAFJK6p6pTmnHcVxDAQUqx7JLakyrkzDJKw'
CHAT_ID = 1110493721  # Update with your chat ID

# Action descriptions (Updated as per provided codes)
ACTION_DESCRIPTIONS = {
    1: "Unlocked 🔓",
    2: "Locked 🔒",
    3: "Unlatch 🔑",
    4: "Lock'n'Go 🔒💨",
    5: "Lock'n'Go with Unlatch 🔒🔑💨",
    6: "Unknown Action 6 ❓",
    7: "Unknown Action 7 ❓",
    253: "Boot Run 🖥️",
    254: "Motor Blocked 🚫",
    255: "Undefined ❓"
}

# Initialize last known action
last_known_action = None

# Define staging actions (those in which the lock is transitioning)
STAGING_ACTIONS = {2, 4, 7}  # Locking, Lock'n'Go, Unlatching

# Function to escape markdown characters
def escape_markdown(text):
    # Escape only necessary markdown special characters in the user name and action
    return text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('[', '\\[').replace(']', '\\]')

async def get_lock_logs():
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}/log?limit=2'  # Fetch only the latest 2 logs
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {Nuki_API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch data from Nuki API. Status code: {response.status_code}")
                return None
            response.raise_for_status()
            data = response.json()

            # Log the entire response for debugging
            logger.info(f"Full response from Nuki API: {data}")

            # Since the response is a list of logs, return it directly
            return data
    except Exception as e:
        logger.error(f"Failed to fetch lock logs: {e}")
        return None

async def send_status_update(context: CallbackContext):
    logs = await get_lock_logs()

    if not logs:
        logger.info("No logs fetched, skipping status update.")
        return  # If no valid log data, skip this update

    # Get the most recent log entry
    latest_log = logs[0]

    # Extract action and user name
    lock_action = latest_log.get('action', None)
    user_name = latest_log.get('name', None)

    if lock_action is None or user_name is None:
        logger.error("No action or name found in the log entry.")
        return

    # Check if the lock action has changed from the last known action
    global last_known_action
    if lock_action == last_known_action:
        logger.info(f"Lock action hasn't changed. Current action: {ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')}")
        return

    # Update the last known action to the current one
    last_known_action = lock_action

    # Get the action description
    action_desc = ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')

    # Extract the date from the log and format it as HH:MM Uhr DD.MM.YY
    log_date = latest_log.get('date', '')
    try:
        # Parse the date string and format it into the desired format
        formatted_date = datetime.fromisoformat(log_date.replace("Z", "")).strftime('%H:%M Uhr %d.%m.%y')
    except ValueError:
        formatted_date = "Unknown Date"

    # Escape markdown special characters for the message text
    message = (f"*{escape_markdown(user_name)}* has *{escape_markdown(action_desc)}*\n"
               f"the Door🚪\n" 
               f"at *{escape_markdown(formatted_date)}*\n")

    try:
        # Send the message with markdown formatting
        logger.info(f"Attempting to send message to chat {CHAT_ID}: {message}")
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'  # This enables markdown for bold, italics, etc.
        )
        logger.info(f"Message sent to chat {CHAT_ID}: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to chat {CHAT_ID}: {e}")

async def start(update: Update, context: CallbackContext):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I am your Nuki Lock Bot. I will keep you updated with the lock status.")

def main():
    """Start the bot and set up the scheduler."""
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Command handler to start the bot
    application.add_handler(CommandHandler('start', start))

    # Scheduler setup for periodic lock status updates
    scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()})
    job = scheduler.add_job(send_status_update, 'interval', seconds=10, args=[application])
    scheduler.start()

    # Start the bot
    logger.info("Starting the bot...")
    application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
