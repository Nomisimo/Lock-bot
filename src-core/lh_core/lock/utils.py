# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:06:39 2025

@author: kolja
"""

import random
from datetime import datetime, time as pytime, timezone
from dataclasses import dataclass, asdict
from enum import Enum

import pytz
from pydantic import BaseModel
from typing import List, Union, Type, TypeVar

tz_local = pytz.timezone("Europe/Berlin")
tz_utc = pytz.utc

def dt_or_none(val: str):
    """ convert to datetime if not None."""
    if isinstance(val, datetime):
        return val
    return (datetime.fromisoformat(val).astimezone(tz_local) 
            if val is not None else None)

def tz_as_local(dt: datetime):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz_local)
    return dt.astimezone(tz_local)

def tz_as_utc(dt: datetime):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz_utc)
    return dt.astimezone(tz_utc)

def nuki_datetime_encoder(dt: datetime) -> str:
    return tz_as_utc(dt).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

T = TypeVar("T", bound="BaseModel")

class NukiModel(BaseModel):

    class Config:
        json_encoders = {datetime: nuki_datetime_encoder}

    def to_json(self):
        return self.model_dump(mode="json", exclude_none=True)
    
    @classmethod
    def from_json(cls: Type[T], data: Union[dict, List[dict]]) -> Union[T, List[T]]:
        if isinstance(data, list):
            return [cls(**item) for item in data]
        return cls(**data)





# deprecated
def dt_to_str(dt: datetime):
    return dt.astimezone(tz_utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# deprecated
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