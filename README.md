# LH Lock Telegram Bot

This project is a Python-based Telegram bot that integrates with the Nuki Smart Lock API to provide real-time updates and status information about your smart lock. The bot can send periodic lock status updates, battery statuses, and more directly to a specified Telegram chat.


ToDo:

- check if last log is known, else generate messages for each new log
- check once every day the state to show battery message when critical
- status message: time, offen/zu
und wer / was gemacht hat in msg im chat als protokoll


- lock -> post action, wait 10s retrive logs
- unlock -> same

next: 
- check if door sensor says closed befor locking the door
- check if door closed before locking the door. 



next:

- code -> generate new keypad code with a custom time interval
- -> abfrage
    - was/wer
    - von/bis
    - code wird zufällig generiert, gesetzt und an admin zurück geschickt.
    
- code wird zurückgeschickt in formatierter nachricht, die direkt weitergeleitet werden kann
- (inkl. anreise-bild)

NEXT PROJEKT
- anfrage bot
- wer bin ich, was brauch ich, welcher tag/zeitraum
- 








## Features

- **Real-Time Lock Updates:** Receive lock action notifications (e.g., Locked, Unlocked, Unlatched) in your Telegram chat.
- **Battery Status Monitoring:** Check the battery levels of your smart lock, keypad, and door sensor.
- **Customizable Logging:** Enable or disable logs for different components.
- **Periodic Updates:** Uses the APScheduler library to fetch lock status at regular intervals.

## Requirements

- Python 3.9+
- Telegram bot token (from [BotFather](https://core.telegram.org/bots#botfather))
- Nuki Smart Lock API token
- Chat ID of the recipient for updates (can be obtained via the Telegram Bot API)

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/nuki-lock-telegram-bot.git
    cd nuki-lock-telegram-bot
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure API Keys and IDs:**
    Update the following constants in the script:
    ```python
    LOCK_ID = YOUR_LOCK_ID
    Nuki_API_KEY = 'your-nuki-api-key'
    TELEGRAM_API_KEY = 'your-telegram-bot-token'
    CHAT_ID = your-telegram-chat-id
    ```

4. **Run the Bot:**
    ```bash
    python Lock-Bot.py
    ```

## Usage

### Telegram Commands
- `/start`: Initialize the bot and receive a welcome message.
- `/Battery`: Get the current battery status of the lock, keypad, and door sensor.

### Periodic Updates
- The bot fetches and sends the lock status every 10 seconds by default. This interval can be adjusted in the script by modifying the `seconds` parameter in the scheduler job:
  ```python
  job = scheduler.add_job(send_status_update, 'interval', seconds=10, args=[application])
  ```

## Customization

### Logging
You can toggle logging for different categories by modifying the `LOGS_ENABLED` dictionary:
```python
LOGS_ENABLED = {
    'general': True,
    'battery': True,
    'lock_status': True,
}
```

### Action Descriptions
Edit or add new action descriptions in the `ACTION_DESCRIPTIONS` dictionary:
```python
ACTION_DESCRIPTIONS = {
    1: "Unlocked 🔓",
    2: "Locked 🔒",
    3: "Unlatch 🔑",
    4: "Lock'n'Go 🔒💨",
    5: "Lock'n'Go with Unlatch 🔒🔑💨",
    6: "Unknown Action 6 ❓",
    7: "Unknown Action 7 ❓",
}
```

## Troubleshooting

### Common Issues

1. **Bot Doesn't Respond:**
   - Ensure the bot token and chat ID are correct.
   - Check your internet connection.
   - Verify that the bot is running and properly configured.

2. **Failed API Requests:**
   - Ensure the Nuki API key is valid.
   - Check the lock ID and permissions for the API key.

## Dependencies

The script uses the following Python libraries:

- `httpx`: For making asynchronous HTTP requests.
- `python-telegram-bot`: For interacting with the Telegram Bot API.
- `apscheduler`: For scheduling periodic tasks.
- `asyncio`: For asynchronous programming.

## License

This project is licensed under the MIT License. Feel free to use and modify it for your purposes.

## Contributions

Contributions are welcome! If you'd like to improve the bot or add features, feel free to submit a pull request.

