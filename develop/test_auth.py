# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 00:06:57 2025

@author: kolja
"""
import logging

from lockbot import config
from lockbot.lock import Nuki
from lockbot.lock.auth import SmartlockAuths


# SETUP
config.load_config("config_dev.cfg")
nuki = Nuki.new()
lock_id = nuki.lock_ids[0]
nuki.logger.setLevel(logging.DEBUG)




""" TODOS:
    - update time range
    - create
    - delete
    - ASync implementation
"""


# AUTHS = nuki.get_auth(lock_id, raw=True)
updated = (
    # SmartlockAuths(AUTHS)
    nuki.get_auth(lock_id, raw=False)
    .by_name("ATest")
    # .set_name("BTest")
    .rotate_code()
    .update_enable(True)
    .updated()
)
# nuki.update_auth(updated.to_json(), raw=True)
nuki.update_auth(updated)
updated

