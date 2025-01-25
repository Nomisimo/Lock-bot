# LH Lock Telegram Bot

This project shall control the garage door of LautisHannover. It uses 
- the Telegram-API to create a bot, that integrates with
- the Nuki Smart Lock API to provide real-time updates and status information about your smart lock. 


## setup and run bot
- install the package via pyproject toml:
```
pip install -e .
```
- update the config.cfg file in the directory accordingly:
    - add API-Keys for NUKI and TELEGRAM
    - add your telegram chat id to the [auth] section.
    - (adjust logging levels for different python modules)

- run the bot. Inside the directory with the config.cfg:
```
python -m lockbot
```
or
```
lockbot
```
### development
- install the package with optional dependencies
```
pip install -e .[dev]
```
- you can download some testdata from the API. This will be saved in "tests/data".
```
lockbot --testdata
```
- you can run pytest from the main directory. This will run the tests defined within the tests subdirectory.
```
pytest
```

## Current features and Changelog
- [x] lock and unlock: send the action to the smartlock
- [x] battery: request info to display the battery status
    - [x] display the battery info when starting the bot
    - [ ] add 24h schedule for checking, whether the battery is critical
- [x] status updates: send notifications, if the lock changes
    - [x] periodically retrieve logs
    - [x] check whether the log was viewed previously (by adding their ids to a deque)
    - [x] send messages for new updates to the chat
    - [x] pin a message with the current lock status
        
## Buglist and Roadmap
- [ ] security- logic: 
    - [ ] check if the door is closed before send lock signal
    - [ ] if the door is open but lock closed: open the lock and send warning
- [ ] keypad
    - [ ] generate new keycodes
    - [ ] set a limited time window for keycodes
    - [ ] reset all keycodes (other than the default one used by us)
    - [ ] build a dialog to request a keycode
    - [ ] format a default text, that could be forwarded to other users
    
- [ ] request bot
    - [ ] create a bot to make a request for LH-equipment.
    - [ ] develop questionaire 
    - [ ] send summary to LH account
    - [ ] create a group with requester, bot and lh account
    - [ ] create entry to google calender
    - [ ] ...

## License

This project is licensed under the MIT License. Feel free to use and modify it for your purposes.

## Contributions

Contributions are welcome! If you'd like to improve the bot or add features, feel free to submit a pull request.

