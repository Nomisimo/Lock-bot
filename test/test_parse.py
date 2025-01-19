# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:27:28 2025

@author: kolja
"""

from lockbot.lock import parse
from lockbot.bot import message
import testdata

from pprint import pprint

def test_parse():
    logs = testdata.logfile()
    
    for log in logs[2:6]:
        print(message.log(log))
        print()
    
    pprint(log)
    # state = testdata.status_unlocked()
    # print(message.battery(state))
    # pprint(state)
    
if __name__ == "__main__":
    test_parse()