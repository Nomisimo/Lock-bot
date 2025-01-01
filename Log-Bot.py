import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import asyncio
from datetime import datetime
import hashlib  # Required for password hashing
from datetime import timedelta



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
}

# Initialize last known action
last_known_action = None

# Toggling logs for different functions
LOGS_ENABLED = {
    'general': True,
    'battery': True,
    'lock_status': False,
}

# Function to escape markdown characters
def escape_markdown(text):
    # Escape only necessary markdown special characters in the user name and action
    return text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('[', '\\[').replace(']', '\\]')

# Log function for toggling log level
def log_message(message, category='general'):
    if LOGS_ENABLED.get(category, False):
        logger.info(message)

# Function to get battery status
async def get_battery_status():
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {Nuki_API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                log_message(f"Failed to fetch data from Nuki API. Status code: {response.status_code}", 'battery')
                return None
            response.raise_for_status()
            data = response.json()
            log_message(f"Full response from Nuki API: {data}", 'battery')
            return data
    except Exception as e:
        log_message(f"Failed to fetch battery data: {e}", 'battery')
        return None

# Function to get lock logs and process lock status
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
                log_message(f"Failed to fetch data from Nuki API. Status code: {response.status_code}", 'lock_status')
                return None
            response.raise_for_status()
            data = response.json()
            log_message(f"Full response from Nuki API: {data}", 'lock_status')
            return data
    except Exception as e:
        log_message(f"Failed to fetch lock logs: {e}", 'lock_status')
        return None

# Function to send lock status update
async def send_status_update(context: CallbackContext):
    logs = await get_lock_logs()

    if not logs:
        log_message("No logs fetched, skipping status update.", 'lock_status')
        return  # If no valid log data, skip this update

    # Get the most recent log entry
    latest_log = logs[0]

    # Extract action and user name
    lock_action = latest_log.get('action', None)
    user_name = latest_log.get('name', None)

    if lock_action is None or user_name is None:
        log_message("No action or name found in the log entry.", 'lock_status')
        return

    # Check if the lock action has changed from the last known action
    global last_known_action
    if lock_action == last_known_action:
        log_message(f"Lock action hasn't changed. Current action: {ACTION_DESCRIPTIONS.get(lock_action, 'Unknown Action ❓')}", 'lock_status')
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
        log_message(f"Attempting to send message to chat {CHAT_ID}: {message}", 'lock_status')
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'  # This enables markdown for bold, italics, etc.
        )
        log_message(f"Message sent to chat {CHAT_ID}: {message}", 'lock_status')
    except Exception as e:
        log_message(f"Failed to send message to chat {CHAT_ID}: {e}", 'lock_status')

# Function to send battery status
async def battery_status(update: Update, context: CallbackContext):
    data = await get_battery_status()

    if not data:
        await update.message.reply_text("Could not fetch battery status from Nuki API.")
        return

    # Extract battery information
    battery_charge = data.get('state', {}).get('batteryCharge', 'Unknown')
    battery_critical = data.get('state', {}).get('batteryCritical', False)
    keypad_battery_critical = data.get('state', {}).get('keypadBatteryCritical', False)
    doorsensor_battery_critical = data.get('state', {}).get('doorsensorBatteryCritical', False)

    # Prepare the message with battery information
    battery_message = (f"*Battery Status*\n"
                       f"*Lock:* {battery_charge}%{' (Critical🪫)' if battery_critical else '🔋'}\n"
                       f"*Keypad:* {'Critical 🪫' if keypad_battery_critical else 'Normal 🔋'}\n"
                       f"*Door Sensor:* {'Critical 🪫' if doorsensor_battery_critical else 'Normal 🔋'}\n")

    try:
        log_message(f"Attempting to send battery status to chat {CHAT_ID}: {battery_message}", 'battery')
        await update.message.reply_text(battery_message, parse_mode='Markdown')
        log_message(f"Battery status sent to chat {CHAT_ID}: {battery_message}", 'battery')
    except Exception as e:
        log_message(f"Failed to send battery status to chat {CHAT_ID}: {e}", 'battery')

# Password and authorization setup
PASSWORD_HASH = hashlib.sha256(b"186262").hexdigest()  # Replace "your_secure_password" with your desired password
authorized_users = {}  # Dictionary to store user IDs and their authorization expiration time

# Helper function to check password
def check_password(input_password: str) -> bool:
    return hashlib.sha256(input_password.encode()).hexdigest() == PASSWORD_HASH

# Command to handle /lock
async def lock_command(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide a password: /lock <password>")
        return

    user_id = update.effective_user.id
    password = context.args[0]

    # Verify password
    if check_password(password):
        # Authorize the user for 10 minutes
        authorized_users[user_id] = datetime.now() + timedelta(minutes=10)
        await update.message.reply_text("You are authorized for 10 minutes to use /lock and /unlock commands.")
        # Delete the password message for security
        await update.message.delete()
    elif user_id in authorized_users and datetime.now() < authorized_users[user_id]:
        # If already authorized, perform the lock action
        url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/lock"
        headers = {'authorization': f'Bearer {NUKI_API_KEY}'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            if response.status_code == 200:
                await update.message.reply_text("The lock has been successfully locked 🔒.")
            else:
                await update.message.reply_text("Failed to lock the door. Please try again.")
    else:
        await update.message.reply_text("Unauthorized. Please provide the correct password: /lock <password>")
        await update.message.delete()

# Command to handle /unlock
async def unlock_command(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide a password: /unlock <password>")
        return

    user_id = update.effective_user.id
    password = context.args[0]

    # Verify password
    if check_password(password):
        # Authorize the user for 10 minutes
        authorized_users[user_id] = datetime.now() + timedelta(minutes=10)
        await update.message.reply_text("You are authorized for 10 minutes to use /lock and /unlock commands.")
        # Delete the password message for security
        await update.message.delete()
    elif user_id in authorized_users and datetime.now() < authorized_users[user_id]:
        # If already authorized, perform the unlock action
        url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/unlock"
        headers = {'authorization': f'Bearer {NUKI_API_KEY}'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            if response.status_code == 200:
                await update.message.reply_text("The lock has been successfully unlocked 🔓.")
            else:
                await update.message.reply_text("Failed to unlock the door. Please try again.")
    else:
        await update.message.reply_text("Unauthorized. Please provide the correct password: /unlock <password>")
        await update.message.delete()
        
        
# Command to start the bot
async def start(update: Update, context: CallbackContext):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I am your Nuki Lock Bot. I will keep you updated with the lock status.")

# Main function to start the bot and schedule jobs
def main():
    """Start the bot and set up the scheduler."""
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Command handler to start the bot
    application.add_handler(CommandHandler('start', start))

    # Command handler to get battery status
    application.add_handler(CommandHandler('Battery', battery_status))
    # Command handler to lock and unlock 
    application.add_handler(CommandHandler('lock', lock_command))
    application.add_handler(CommandHandler('unlock', unlock_command))


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
