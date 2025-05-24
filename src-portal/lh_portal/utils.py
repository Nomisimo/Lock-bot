# -*- coding: utf-8 -*-
"""
Created on Sat May 24 22:54:00 2025

@author: kolja
"""

from datetime import datetime, UTC
from pydantic import BaseModel

def date_fmt(dt: datetime) -> str:
    """ string representation relativ to current time."""
    now = datetime.now(tz=UTC)
    tdif = now - dt
    tmin = tdif.seconds//60
    if tdif.days == 0 and tmin < 60:
        return f"{tmin} min ago"
    elif tdif.days == 0 and tmin < 300:
        return f"{tmin//60}h{tmin%60}min ago"
    elif tdif.days == 0:
        return dt.strftime("%X")
    elif tdif.days == 1:
        return dt.strftime("%X (gestern)")
    return dt.strftime("%X (%x)")


class AcceptedResponse(BaseModel):
    message: str