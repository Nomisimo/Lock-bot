# -*- coding: utf-8 -*-
"""
Created on Sun May 18 14:59:28 2025

generic json caching functions.

@author: kolja
"""

from lh_core import config

from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime, UTC
from pathlib import Path
import json
import logging

from pydantic import BaseModel, TypeAdapter
# MODEL = TypeVar("MODEL", bound=BaseModel)
MODEL = TypeVar("MODEL", bound=Union[BaseModel, TypeAdapter])


def get_cache_path(filepath: Path):
    filepath = Path(filepath).resolve()
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    return filepath


def save_cache(filepath: Path, data: MODEL, raw=False):
    filepath = get_cache_path(filepath)
    
    if raw:
        json_data = data
    elif isinstance(data, BaseModel):
        json_data = data.model_dump(mode="json", exclude_none=True)
    elif isinstance(data, list):
        json_data = [item.model_dump(mode="json", exclude_none=True) for item in data]
    else:
        raise ValueError("data of type {type(data)} could not be cached.")
    
    cache = {
        "timestamp": datetime.now(UTC).isoformat(),
        "data": json_data
    }
    
    with  filepath.open("w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2, ensure_ascii=False)
    logging.info(f"saved @ {filepath}")
    

def load_cache(filepath: Path, model: Type[MODEL], raw: bool=False) -> (datetime, Optional[List[MODEL]]):
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
    
    if raw:
        return timestamp, cache["data"]
    if isinstance(model, TypeAdapter):
        return timestamp, model.validate_python(cache["data"])
    elif issubclass(model, BaseModel):
        return timestamp,  model.validate(cache["data"])
    else:
        raise TypeError(f"model has to by TypeAdapter or BaseModel, but is '{type(model)}'")



# TODO: max AGE
    # , max_age: int = 3600
    # if datetime.utcnow() - timestamp > timedelta(seconds=max_age):
    #     logging.warning("cache to old")
    #     return None