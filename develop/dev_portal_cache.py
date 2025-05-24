# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:46:01 2025

@author: kolja
"""
from lh_core import cache, config, lock, tracker
from lh_portal.dependencies import cache_logs, cache_dir, cache_tracker, cache_state
from pathlib import Path


# async def save_tracker_cache() -> None: # pragma: no cover
#     """Run!"""

#     config.load_config()
#     filepath = cache_tracker(cache_dir())
#     # filepath = Path(config.get("portal", "cache")) / "CACHE_tile.json"

#     data = await tracker.retrieve_data()    
#     cache.save_cache(filepath, data)
#     dt, cdata = cache.load_cache(filepath, tracker.TileList)
    
#     t1, t2 = data[0], cdata[0]
#     assert (t1 == t2), str([t1, t2])
        
# main()
# if __name__ == "__main__": # pragma: no cover
    # import asyncio
    # asyncio.run(save_tracker_cache())

def save_state_cache():
    config.load_config("config_lautis.cfg")
    filepath = cache_state(cache_dir())
    
    nuki = lock.Nuki()
    # nuki.retrieve_smartlock_ids()
    data = nuki.get_smartlock(lock_id=nuki.default_id)
    cache.save_cache(filepath, data)

def save_log_cache():
    config.load_config("config_lautis.cfg")
    filepath = cache_logs(cache_dir())
    
    nuki = lock.Nuki()
    # nuki.retrieve_smartlock_ids()
    data = nuki.get_logs(lock_id=None, limit=10)
    cache.save_cache(filepath, data)
    

if __name__ == "__main__":
    save_log_cache()
    save_state_cache()
