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
