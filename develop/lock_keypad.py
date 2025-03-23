# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 19:37:08 2025

@author: kolja
"""

from lockbot import config, Nuki
from pprint import pprint
from lockbot.lock import urls
import logging

config.load_config("config_dev.cfg")
nuki = Nuki.new()
lock_id = nuki.lock_ids[0]
nuki.logger.setLevel(logging.DEBUG)

# AUTHS = nuki.get_auth(lock_id, raw=True)

#%%
#config.load_config("config_dev.cfg")
from datetime import datetime
from lockbot.lock.model import dt_or_none, dt_to_str

from datetime import time as pytime
def total_minutes(dt: datetime | pytime) -> int:
    return dt.minute + dt.hour*60

def get_codes(auths: list[dict]) -> dict[str, dict]:
    return {a.get("code"): a for a in auths if a.get("code") is not None}

def get_names(auths: list[dict]) -> dict[str, dict]:
    return {a.get("name"): a for a in auths if a.get("name") is not None}


def auth_get_name(name: str, auths: list[dict]) -> dict | None:
    names = get_names(auths)
    if name in names:
        return names.get(name)
    return None
    
def auth_check_name(name: str, auths: list[dict]) -> bool:
    return name in get_names(auths)


def auth_get_code(code: int, auths: list[dict]) -> dict | None:
    codes = get_codes(auths)
    if code in codes:
        return codes.get(code)
    return None
    
def auth_check_code(code, auths):
    return code in get_codes(auths)


def auth_update_name(old: str, new: str):
    logging.info("update name")
    AUTHS = nuki.get_auth(lock_id, raw=True)
    
    a = auth_get_name(old, AUTHS)
    if not a:
        logging.warning("name not found")
        return False
    if auth_check_name(new, AUTHS):
        logging.warning("name already exists")
        return False
    a["name"] = new
    val = nuki.update_auth(lock_id, auth_id=a["id"], data=a, raw=True)
    if val:
        logging.info("name updated")
    return val

def auth_enable(name, enable: bool = None):
    AUTHS = nuki.get_auth(lock_id, raw=True)
    a = auth_get_name(name, AUTHS)
    
    if not a:
        logging.warning(f"{name=} not found")
        return False
    if enable is None: # toggle
        a["enabled"] = not a["enabled"]
    else:
        a["enabled"] = enable
        
    val = nuki.update_auth(lock_id, auth_id=a["id"], data=a, raw=True)
    logging.info(f"{name=} set enabled={a['enabled']}")
    return val

# auth_update_name("testing", "TESTING")    
# auth_enable("TESTING")

### ZEITBEGRENZUNG: braucht den ganzen Block
def auth_set_dt(name: str, from_date: datetime = None, until_date: datetime = None):
    AUTHS = nuki.get_auth(lock_id, raw=True)
    a = auth_get_name(name, AUTHS)
    if not a:
        logging.warning(f"{name=} not found")
        return False
    print(a)
    if from_date is None:
        a["allowedWeekDays"] = 0
        a["allowedFromTime"] = None
        a["allowedUntilTime"] = None
        a["allowedFromDate"] = None
        a["allowedUntilDate"] = None
    else:
         
        a["allowedWeekDays"] = 127
        a["allowedFromTime"] = 0
        a["allowedUntilTime"] = 0
        a["allowedFromDate"] = dt_to_str(from_date)
        a["allowedUntilDate"] = dt_to_str(until_date)
        
    val = nuki.update_auth(lock_id, auth_id=a["id"], data=a, raw=True)
    logging.info(f"{name=} set date={from_date, until_date}")
    # return val


    
# auth_enable("TESTING", True)
# d1 = datetime(2025, 4, 21, 8)
# d2 = datetime(2025, 4, 21, 18)
# d1, d2 = None, None
# auth_set_dt("TESTING", d1, d2)

    


# TODO: 
# new code generation, 
# old code deletion, 
# code update

# auth options:
# show all
# show name
# create auth
# update name
# update code
# enable auth
# set time
# delete auth


import random

random.choice()




# a = AUTHS[-3]
# a["name"] = "testing"
# new = {
#   "name": "testing",
# #   "allowedFromDate": "2025-03-11T19:31:33.359Z",
# #   "allowedUntilDate": "2025-03-11T19:31:33.359Z",
# #   "allowedWeekDays": 127,
# #   "allowedFromTime": 0,
# #   "allowedUntilTime": 0,
# #   "accountUserId": 0,
# #   "remoteAllowed": True,
# #   "smartActionsEnabled": True,
#   "type": 13,
#    "code": 115119
# }
# url = urls.url_auth(lock_id, auth_id=a["id"])
# nuki.post_request(url, json=a)





# print([(a["id"], a["name"]) for a in auths])

# url = urls.url_auth(lock_id, a["id"])
# r = nuki.post_request(url, json=a | {"name":"updated name"})


# n = nuki.get_auth(lock_id, a["id"], raw=True)


# print(n["name"])