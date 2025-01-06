# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:27:28 2025

@author: kolja
"""

from lockbot.lock import parse
import testdata


def test_parse():
    logs = testdata.logfile()
    
    for log in logs[2:6]:
        print(parse.msg_log(log))
        print()
    
    state = testdata.status_unlocked()
    print(parse.msg_battery(state))
    
if __name__ == "__main__":
    test_parse()