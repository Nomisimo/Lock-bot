# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
from lockbot import config
from lockbot import Nuki
        
def test():
    
    config.load_config()
    nuki = Nuki()
    
    
if __name__ == "__main__":
    test()
    