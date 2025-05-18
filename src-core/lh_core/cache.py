# -*- coding: utf-8 -*-
"""
Created on Sun May 18 14:59:28 2025

@author: kolja
"""

from lh_core import config

from typing import Type, TypeVar, List, Optional
from datetime import datetime, UTC
from pathlib import Path
import json
import logging

from pydantic import BaseModel
MODEL = TypeVar("MODEL", bound=BaseModel)


def get_cache_path(filepath: Path):
    filepath = Path(filepath).resolve()
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    return filepath


def save_cache(filepath: Path, data: MODEL):
    filepath = get_cache_path(filepath)
    
    cache = {
        "timestamp": datetime.now(UTC).isoformat(),
        "data": [item.model_dump(mode="json") for item in data]
    }
    
    with  filepath.open("w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2, ensure_ascii=False)
    logging.info(f"saved @ {filepath}")
    

def load_cache(filepath: Path, model: Type[MODEL]) -> (datetime, Optional[List[MODEL]]):
    filepath = get_cache_path(filepath)
    if not filepath.exists:
        logging.warning("cache not found.")
        return None, None
    
    with filepath.open("r", encoding="utf-8") as file:
        try:
            cache = json.load(file)
            timestamp = datetime.fromisoformat(cache["timestamp"])
        except Exception as e:
            logging.warning(f"error while cache loading: {e}")
            return None, None
    try:
        
        data = model.validate_python(cache["data"])
    except Exception as e:
        logging.warning(f"error while parsing: {e}")
        return None, None
    return timestamp, data



# TODO: max AGE
    # , max_age: int = 3600
    # if datetime.utcnow() - timestamp > timedelta(seconds=max_age):
    #     logging.warning("cache to old")
    #     return None