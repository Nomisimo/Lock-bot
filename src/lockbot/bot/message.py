# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:06:26 2025

@author: kolja
"""
from datetime import datetime

from lockbot.lock.const import ROOM_NAME_DE, LOG_STATE, DOOR_STATE, ACTION, ACTION_DE
from lockbot.lock import model
# from lockbot

def timestamp():
    return datetime.now().strftime("%T")
    

def emoji_battery(critical=False):
    return '🪫' if critical else '🔋'

def battery(state = model.Smartlock):
    msg = (
        f"battery status:\n"
        f"- lock   {emoji_battery(state.state.batteryCritical)}({state.state.batteryCharge}%)\n"
        f"- keypad {emoji_battery(state.state.keypadBatteryCritical)}\n "
        f"- sensor {emoji_battery(state.state.doorsensorBatteryCritical)}\n"
        f"(checked: {state.updateDate.strftime('%T')})"
        )
    return msg


def emoji_action(state: LOG_STATE, action: ACTION):
    if state != LOG_STATE.success:
        return "❌"
    if action == ACTION.lock:
        return "🔒"
    if action == ACTION.unlock:
        return "🔓"
    return "❔"

def log(data: model.LogEntry, user="lockbot"):
    time = data.date.strftime('%T')
    user = data.name if hasattr(data, 'name') and data.name else "Auto Lock"
    action = emoji_action(data.state, data.action) + data.action.name
    # Fetch the German translation for the action using the ACTION_DE enum
    action_de = ACTION_DE.__members__.get(data.action.name, ACTION_DE.unknown).value    
    room = ROOM_NAME_DE.Garage21.value  # Returns "Garage21"

    
    if data.action.value in [240, 241]:
        msg = f"{room} um {time} 🕗\n{action_de}"
    else:
        msg = f"{room} um {time} 🕗\n{action_de}\n von {user}"
    
    if (state := data.state) != LOG_STATE.success:
        msg += f"\n {state.name}"
    
    return msg


