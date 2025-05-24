# -*- coding: utf-8 -*-
"""
Created on Thu May 15 20:43:31 2025

@author: kolja
"""
from typing import Annotated
from pathlib import Path

from fastapi import Depends
from lh_core import config, tracker, lock


def cache_dir() -> Path:
    path_cache = Path(config.get("portal", "cache"))
    return path_cache

def cache_tracker(path_cache: Annotated[Path, Depends(cache_dir)]) -> Path:
    return path_cache / tracker.CACHE_NAME

def cache_logs(path_cache: Annotated[Path, Depends(cache_dir)]) -> Path:
    return path_cache / lock.model.CACHE_NAME_LOGS

def cache_state(path_cache: Annotated[Path, Depends(cache_dir)]) -> Path:
    return path_cache / lock.model.CACHE_NAME_STATE

def cache_auth(path_cache: Annotated[Path, Depends(cache_dir)]) -> Path:
    return path_cache / lock.model.CACHE_NAME_AUTH