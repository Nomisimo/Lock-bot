# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 00:29:42 2025

@author: kolja
"""

from lockbot import config
from lockbot.tool import testdata
from lockbot.lock.model import SmartlockAuth


config.load_config("config_dev.cfg")
raw = testdata.load_auths()

SmartlockAuth(**raw[0])
