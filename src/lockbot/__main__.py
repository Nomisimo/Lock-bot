# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 23:06:16 2025

@author: kolja
"""
import os

def greet():
    user = os.getlogin()
    print(f"Hello {user}, lockbot is installed.")
    
if __name__ == "__main__":
    greet()