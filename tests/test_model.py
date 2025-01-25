# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 23:30:46 2025

@author: kolja
"""

from lockbot import config
from lockbot.tool import testdata
from lockbot.lock import model


config.load_config("config_pytest.cfg")

def test_log_conversion():
    data = testdata.load_logfile()
    for log in data:
        
        converted = model.LogEntry(**log).to_json()
        assert log == converted

def test_state_conversion():
    state = testdata.load_status("lock")["state"]
    converted = model.SmartlockState(**state).to_json()
    assert state == converted
    
    state = testdata.load_status("unlock")["state"]
    converted = model.SmartlockState(**state).to_json()
    assert state == converted
    
def test_smartlock_conversion():
    state = testdata.load_status("lock")
    converted = model.Smartlock(**state).to_json()
    assert state == converted
    
    state = testdata.load_status("unlock")
    converted = model.Smartlock(**state).to_json()
    assert state == converted
    
def test_smartlock_auth():
    auths = testdata.load_auths()
    for auth in auths:
        converted = model.SmartlockAuth(**auth).to_json()
        assert auth == converted
    
