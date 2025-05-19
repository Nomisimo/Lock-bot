# -*- coding: utf-8 -*-
"""
Created on Mon May 19 10:47:47 2025

@author: kolja
"""
import pytest
from pathlib import Path
from datetime import datetime

from lh_core import config
from lh_core.tool import testdata
from lh_core import tracker, cache

config.load_config("config_pytest.cfg")
    
@pytest.mark.asyncio
async def test_retrieve_data(tmp_path: Path):
    """Test that tile data can be retrieved and saved as JSON."""
    config.load_config()

    data = await tracker.retrieve_data()
    assert data, "No data retrieved"
    assert isinstance(data, list)
    assert hasattr(data[0], "model_dump")  # Assuming Pydantic models

    filepath = tmp_path / "CACHE_tile.json"
    cache.save_cache(filepath, data)

    assert filepath.exists(), "Cache file was not created"


def test_reload_data(tmp_path: Path):
    """Test that saved tile data can be reloaded and matches original."""
    # Simulate saved cache

    original = tracker.TileDevice(
        name="Test",
        latitude=52.1,
        longitude=9.7,
        last_timestamp="2025-05-19T12:00:00Z",
        altitude=60.0,
        accuracy=10.0,
        archetype="OTHER",
        dead=False,
        firmware_version="1.0",
        hardware_version="1.0",
        kind="TILE",
        lost=False,
        lost_timestamp="1970-01-01T00:00:00Z",
        ring_state="STOPPED",
        uuid="abc123",
        visible=True,
        voip_state="OFFLINE"
    )

    filepath = tmp_path / "CACHE_tile.json"
    cache.save_cache(filepath, [original])

    timestamp, loaded = cache.load_cache(filepath, tracker.CACHE_MODEL)

    assert isinstance(loaded, list)
    assert len(loaded) == 1
    assert loaded[0] == original
    assert isinstance(timestamp, datetime)