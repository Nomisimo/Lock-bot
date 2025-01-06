# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 21:37:38 2025

@author: kolja
"""
from datetime import datetime
import pytz

from lockbot.lock.const import (
    ACTION, 
    ADMINPIN_STATE,
    DEVICE_TYPE, 
    DOOR_STATE,
    LOG_STATE, 
    LOG_SOURCE,
    LOCK_MODE,
    LOCK_STATE,
    SERVER_STATE,
    TRIGGER
    )

tz_local = pytz.timezone("Europe/Berlin")

def convert_timestamp(data: str) -> datetime:
    return datetime.fromisoformat(data).astimezone(tz_local)
    
def log(data: dict) -> dict:
    data["deviceType"] = DEVICE_TYPE(data.get("deviceType", DEVICE_TYPE.unknown))
    data["action"] = ACTION(data.get("action", ACTION.unknown))
    data["trigger"] = TRIGGER(data.get("trigger", TRIGGER.unknown))
    data["state"] = LOG_STATE(data.get("state", LOG_STATE.unknown_error))
    data["source"] = LOG_SOURCE(data.get("source", LOG_SOURCE.unknown))
    data["date"] = convert_timestamp(data["date"])
    return data

def logs(data: list[dict]) -> list[dict]:
    return [log(d) for d in data]

def state(data, reduce=True):
    if reduce:
        for key in ("config", "advancedConfig", "currentSubscription"):
            data.pop(key)
            
    data["type"] = DEVICE_TYPE(data["type"])
    data["serverState"] = SERVER_STATE(data.get("serverState"))
    data["adminPinState"] = ADMINPIN_STATE(data.get("adminPinState"))
    
    data["creationDate"] = convert_timestamp(data.get("creationDate"))
    data["updateDate"] = convert_timestamp(data.get("updateDate"))
    
    state = data.pop("state")
    state["mode"] = LOCK_MODE(state.get("mode"))
    state["state"] = LOCK_STATE(state.get("state"))
    state["trigger"] = TRIGGER(state.get("trigger"))
    state["lastAction"] = ACTION(state.get("lastAction"))
    state["doorState"] = DOOR_STATE(state.get("doorState"))
    for key, val in state.items():
        data[key] = val
    return data


def emoji_battery(critical=False):
    return '🪫' if critical else '🔋'

def msg_battery(data):
    status = state(data)
    msg = (
        "**battery status**\n"
        f"- lock   {emoji_battery(status['batteryCritical'])}({status['batteryCharge']}%)\n"
        f"- keypad {emoji_battery(status['batteryCritical'])}\n"
        f"- sensor {emoji_battery(status['batteryCritical'])}"
        f"({status['updateDate'].strftime('%T')})"
        )
    return msg

def emoji_action(state, action):
    if state != LOG_STATE.success:
        return "❌"
    if action == ACTION.lock:
        return "🔒"
    if action == ACTION.unlock:
        return "🔓"
    return "❔"
    

def msg_log(data, user="lockbot"):
    l = log(data)
    time = l['date'].strftime('%T')
    user = user if l["name"] == "Lock Bot 🤖" else l["trigger"].name
    action = emoji_action(l["state"], l["action"]) + l["action"].name
    msg = f"*LOG {time}*\n{action} by {user}"
    if (state := l["state"]) != LOG_STATE.success:
        msg +=f"\n {state.name}"
    return msg
