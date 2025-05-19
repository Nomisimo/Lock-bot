# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 00:06:57 2025

@author: kolja
"""
import logging
from datetime import datetime, timezone

from lh_core import config
from lh_core.lock import Nuki, urls
from lh_core.lock.auth import SmartlockAuths, SmartlockAuth, SmartlockAuthCreate
from lh_core.lock.const import AUTH_TYPE

from pprint import pprint
t1 = datetime(2025,4,10, 10)
t2 = datetime(2025,4,10, 15)

# SETUP
config.load_config("config_dev.cfg")
nuki = Nuki.new()
lock_id = nuki.lock_ids[0]
nuki.logger.setLevel(logging.DEBUG)


""" TODOS:
    - ASync implementation
"""
NAME = "string"

#%% create

AUTHS = nuki.get_auth(lock_id)

new = (
   AUTHS.create(NAME, lock_id)
   # .set_period(t1,t2)
   .created()
   )
val = nuki.put_auth(new)
print(val, new)

#%% update
AUTHS = nuki.get_auth(lock_id)

updated = (
    AUTHS
    .by_name(NAME)
    # .set_name("BTest")
    .rotate_code()
    # .update_enable()
    # .set_period(t1,t2)
    # .clear_period()
    .updated()
)
val = nuki.post_auth(updated)
print(val, updated)

#%% delete
AUTHS = nuki.get_auth(lock_id)

selected = AUTHS.delete(NAME)
val = nuki.del_auth(selected)
print(val, selected)

#%%
AUTHS.auths
