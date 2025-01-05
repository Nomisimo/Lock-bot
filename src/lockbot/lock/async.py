# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:43:22 2025

@author: kolja
"""

import logging
import asyncio
import httpx


from lockbot import config

logger = logging.getLogger(__name__)

async def get_lock_status():
    LOCK_ID = config.get("nuki", "LOCK_ID")
    API_KEY = config.get("nuki", "API_KEY")
    
    
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch battery data. Status code: {response.status_code}")
                return None
            data = response.json()
            pprint(data)
            return data
    except Exception as e:
        logger.error(f"Failed to fetch battery data: {e}")
        return None