# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 23:30:46 2025

@author: kolja
"""

from lh_core import config
from lh_core.tool import testdata
from lh_core import lock


config.load_config("config_pytest.cfg")

def test_log_conversion():
    data = testdata.load_logfile()
    for log in data:
        
        converted = lock.SmartlockLog(**log).to_json()
        assert log == converted

def test_state_conversion():
    state = testdata.load_status("lock")["state"]
    converted = lock.SmartlockState(**state).to_json()
    assert state == converted
    
    state = testdata.load_status("unlock")["state"]
    converted = lock.SmartlockState(**state).to_json()
    assert state == converted
    
def test_smartlock_conversion():
    state = testdata.load_status("lock")
    converted = lock.Smartlock(**state).to_json()
    assert state == converted
    
    state = testdata.load_status("unlock")
    converted = lock.Smartlock(**state).to_json()
    assert state == converted
    
def test_smartlock_auth():
    auths = testdata.load_auths()
    for auth in auths:
        converted = lock.SmartlockAuth(**auth).to_json()
        assert auth == converted
    
