# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:06:39 2025

@author: kolja
"""

import random
from datetime import datetime, time as pytime
from dataclasses import dataclass, asdict
from enum import Enum

import pytz

tz_local = pytz.timezone("Europe/Berlin")
tz_utc = pytz.utc


def dt_to_str(dt: datetime):
    return dt.astimezone(tz_utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def dt_or_none(val: str):
    """ convert to datetime if not None."""
    if isinstance(val, datetime):
        return val
    return (datetime.fromisoformat(val).astimezone(tz_local) 
            if val is not None else None)

def convert_to_json(da: object) -> dict:
    """ convert dataclass back to original json dict."""
    res = asdict(da)
    for k, v in res.items():
        if isinstance(v, Enum):
            res[k] = v.value
        if isinstance(v, datetime):
            res[k] = dt_to_str(v)
    # sort out not set optional values
    res = {k: v for k,v in res.items() if v is not None}
    return res


def generate_code(): 
    return int("".join(str(i) for i in random.choices(range(1,10), k=6)))

def total_minutes(dt: datetime | pytime) -> int:
    return dt.minute + dt.hour*60