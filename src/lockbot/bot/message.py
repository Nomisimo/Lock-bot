# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:06:26 2025

@author: kolja
"""
from datetime import datetime

from lockbot.lock.const import LOG_STATE, DOOR_STATE, ACTION
from lockbot.lock import parse


def timestamp():
    return datetime.now().strftime("%T")
    

def emoji_battery(critical=False):
    return '🪫' if critical else '🔋'

def battery(data: dict):
    status = parse.state(data)
    msg = (
        f"battery status:\n"
        f"- lock   {emoji_battery(status['batteryCritical'])}({status['batteryCharge']}%)\n"
        f"- keypad {emoji_battery(status['keypadBatteryCritical'])}\n "
        f"- sensor {emoji_battery(status['doorsensorBatteryCritical'])}\n"
        f"(checked: {status['updateDate'].strftime('%T')})"
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

def log(data: dict, user="lockbot"):
    """ data = single log, user = telegram effective_user.username."""
    l = parse.log(data)
    time = l['date'].strftime('%T')
    user = user if l["name"] == "Lock Bot 🤖" else l["trigger"].name
    action = emoji_action(l["state"], l["action"]) + l["action"].name
    msg = f"[{time}]\n{action} by {user}"
    if (state := l["state"]) != LOG_STATE.success:
        msg +=f"\n {state.name}"
    return msg
