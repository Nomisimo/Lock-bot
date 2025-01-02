import logging

# Nuki API Configuration
LOCK_ID = 17968122341
NUKI_API_KEY = '748c83fab5c4b45224d45025555a31ff9d6b57dff9aa1765703916611c078a2536085b5474b68312'

# Telegram bot configuration
TELEGRAM_API_KEY = '7993283863:AAFJK6p6pTmnHcVxDAQUqx7JLakyrkzDJKw'
CHAT_ID = 1110493721

# List of authorized chat IDs
AUTHORIZED_CHAT_IDS = [1110493721]

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_message(message, category='general'):
    logger.info(f"[{category.upper()}] {message}")

