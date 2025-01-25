# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 21:42:40 2025

@author: kolja
"""
from enum import Enum
from dataclasses import dataclass, asdict, field
from datetime import datetime

from lockbot.lock import const
import testdata

from pprint import pprint

    
    
from lockbot.lock.model import LogEntry, SmartlockState, Smartlock
    
def compare_dicts(src, dst):
    for k in (set(src) | set(dst)):
        if k in src and k not in dst:
            print(k, "in src but not in dst", src[k])
        elif k not in src and k in dst:
            print(k, "not in src but in dst", dst[k])
    
        elif not dst[k] == src[k]:
            print(k)
            pprint(dst[k])
            pprint(src[k])


def test_log_conversion():
    data = testdata.logfile()
    for log in data:
        compare_dicts(log, LogEntry(**log).to_json())
    print("finished log comparison")
        
def test_state_conversion():
    
    state = testdata.status_locked()["state"]
    compare_dicts(state, SmartlockState(**state).to_json())
    state = testdata.status_unlocked()["state"]
    compare_dicts(state, SmartlockState(**state).to_json())
    print("finished log comparison")

        
def test_smartlock_conversion():
    state = testdata.status_locked()
    compare_dicts(state, Smartlock(**state).to_json())
    state = testdata.status_unlocked()
    compare_dicts(state, Smartlock(**state).to_json())
    print("finished log comparison")
        
# def test_smartlock_auth():
#     auths = testdata.auths()
#     for auth in auths:
#         pprint(SmartlockAuth(**auth))
#         compare_dicts(auth, SmartlockAuth(**auth).to_json())
        


if __name__ == "__main__":
    test_log_conversion()
    test_state_conversion()
    test_smartlock_conversion()
    # test_smartlock_auth()