import httpx
import logging

from lockbot import config

logger = logging.getLogger(__name__)

# Define allowed chat IDs
# ALLOWED_CHAT_IDS = {CHAT_ID}  # Use a set for efficient membership checking

# Chat ID validation decorator
def validate_chat_id(func):
    async def wrapper(update, context, *args, **kwargs):
        ALLOWED_IDS = config.get_authorized()

        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_IDS:
            logger.info(f"Unauthorized access attempt from chat ID {chat_id}.")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Function to get lock logs and process lock status
async def get_lock_logs():
    LOCK_ID = config.get("nuki", "LOCK_ID")
    API_KEY = config.get("nuki", "API_KEY")
    
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}/log?limit=2'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch data from Nuki API. Status code: {response.status_code}")
                return None
            data = response.json()
            logger.info(f"Full response from Nuki API: {data}")
            return data
    except Exception as e:
        logger.error(f"Failed to fetch lock logs: {e}")
        return None


# Function to send lock action (lock/unlock)
async def send_lock_action(action, update=None, context=None):
    LOCK_ID = config.get("nuki", "LOCK_ID")
    API_KEY = config.get("nuki", "API_KEY")
    
    url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/{action}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)

        if response.status_code == 204:
            message = f"The door was successfully {action}ed. 🚪✅"
        elif response.status_code == 400:
            message = f"Bad request: Invalid parameters for {action}ing the lock. ❌"
        elif response.status_code == 401:
            message = f"Authorization failed: Please check your API key. ❌"
        elif response.status_code == 405:
            message = f"Action not allowed: {action.capitalize()}ing is not permitted. ❌"
        else:
            message = f"Unexpected error: {response.status_code}. Please try again. ❌"

        logger.info(f"API Response: {response.status_code} - {response.text}")

        if update and context:
            await update.message.reply_text(message)
        return response.status_code == 204

    except Exception as e:
        logger.error(f"Error sending lock action: {e}")
        if update and context:
            await update.message.reply_text("An error occurred while processing the request. Please try again later.")
        return False

# Function to get battery status
async def get_battery_status():
    LOCK_ID = config.get("nuki", "LOCK_ID")
    API_KEY = config.get("nuki", "API_KEY")
    
    
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch battery data. Status code: {response.status_code}")
                return None
            data = response.json()
            logger.info(f"Full response from Nuki API: {data}")
            return data
    except Exception as e:
        logger.error(f"Failed to fetch battery data: {e}")
        return None


# Command to lock the door
@validate_chat_id
async def lock_command(update, context):
    success = await send_lock_action("lock", update, context)
    logger.info(
        "Lock command executed successfully." if success else "Lock command failed.",
    )

# Command to unlock the door
@validate_chat_id
async def unlock_command(update, context):
    success = await send_lock_action("unlock", update, context)
    logger.info(
        "Unlock command executed successfully." if success else "Unlock command failed.",
    )
