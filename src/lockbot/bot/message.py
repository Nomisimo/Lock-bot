# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:06:26 2025

@author: kolja
"""
from datetime import datetime

from lockbot.lock.const import LOG_STATE, DOOR_STATE, ACTION
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
    """ data = single log, user = telegram effective_user.username."""
    
    time = data.date.strftime('%T')
    user = user if data.name == "Lock Bot 🤖" else data.trigger.name
    action = emoji_action(data.state, data.action) + data.action.name
    msg = f"[{time}]\n{action} by {user}"
    if (state := data.state) != LOG_STATE.success:
        msg +=f"\n {state.name}"
    return msg
