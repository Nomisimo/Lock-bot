# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import logging
from pprint import pprint
from typing import Optional, Union, List

from lh_core import config, cache, lock
# from lh_core import Nuki

def test():
    logging.info("syncronous")    
    config.load_config("config_lautis.cfg")
    nuki = lock.Nuki()
    nuki.retrieve_smartlock_ids()
    nuki.set_default_lock()
    
    res = nuki.get_logs(lock_id=None, raw=False, limit=2)
    # res = nuki.get_smartlock(raw=True)
    pprint(res)
    

from lh_portal import dependencies
from datetime import datetime, UTC, timedelta


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
    

def parse_cache():
    config.load_config("config_lautis.cfg")
    filepath = dependencies.cache_logs(dependencies.cache_dir())

    # dt, data = cache.load_cache(filepath, lock.SmartlockLogList)
    # dates = [d.date for d in data]
    dates = [
        datetime.now(tz=UTC) - timedelta(minutes=4),
        datetime.now(tz=UTC) - timedelta(hours=4, minutes=10),
        datetime.now(tz=UTC) - timedelta(hours=8, minutes=10),
        datetime.now(tz=UTC) - timedelta(days=1),

        datetime.now(tz=UTC) - timedelta(days=4),
        
        
        ]
    
    for d in dates:
        pprint([d, date_fmt(d)])
    

if __name__ == "__main__":
    # test()
    parse_cache()