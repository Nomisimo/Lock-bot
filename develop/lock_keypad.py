# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 19:37:08 2025

@author: kolja
"""

from lockbot import config, Nuki
from pprint import pprint
from lockbot.lock import urls

config.load_config("config_dev.cfg")
nuki = Nuki.new()
lock_id = nuki.lock_ids[0]
# nuki.post_lock(lock_id)
auths = nuki.get_auth(lock_id, raw=True)

#%%
config.load_config("config_dev.cfg")

a = auths[-1]


def key_new():
    pass

def key_update(name=False, code=False):
    pass

def key_delete():
    pass

new = {
  "name": "string",
#   "allowedFromDate": "2025-03-11T19:31:33.359Z",
#   "allowedUntilDate": "2025-03-11T19:31:33.359Z",
#   "allowedWeekDays": 127,
#   "allowedFromTime": 0,
#   "allowedUntilTime": 0,
#   "accountUserId": 0,
#   "remoteAllowed": True,
#   "smartActionsEnabled": True,
  "type": 13,
  "code": 115118
}
# url = urls.url_auth(lock_id, a["id"])
# nuki.del_request(url)
a

# print([(a["id"], a["name"]) for a in auths])

# url = urls.url_auth(lock_id, a["id"])
# r = nuki.post_request(url, json=a | {"name":"updated name"})


# n = nuki.get_auth(lock_id, a["id"], raw=True)


# print(n["name"])