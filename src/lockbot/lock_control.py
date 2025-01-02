import httpx
from config import LOCK_ID, NUKI_API_KEY, CHAT_ID, log_message

# Define allowed chat IDs
ALLOWED_CHAT_IDS = {CHAT_ID}  # Use a set for efficient membership checking

# Chat ID validation decorator
def validate_chat_id(func):
    async def wrapper(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_CHAT_IDS:
            log_message(f"Unauthorized access attempt from chat ID {chat_id}.", "security")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Function to send lock action (lock/unlock)
async def send_lock_action(action, update=None, context=None):
    url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/{action}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {NUKI_API_KEY}",
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

        log_message(f"API Response: {response.status_code} - {response.text}", "lock_status")

        if update and context:
            await update.message.reply_text(message)
        return response.status_code == 204

    except Exception as e:
        log_message(f"Error sending lock action: {e}", "lock_status")
        if update and context:
            await update.message.reply_text("An error occurred while processing the request. Please try again later.")
        return False

# Command to lock the door
@validate_chat_id
async def lock_command(update, context):
    success = await send_lock_action("lock", update, context)
    log_message(
        "Lock command executed successfully." if success else "Lock command failed.",
        "lock_status",
    )

# Command to unlock the door
@validate_chat_id
async def unlock_command(update, context):
    success = await send_lock_action("unlock", update, context)
    log_message(
        "Unlock command executed successfully." if success else "Unlock command failed.",
        "lock_status",
    )
