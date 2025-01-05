# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:46:04 2025

@author: kolja
"""
from http import HTTPStatus
import logging

logger = logging.getLogger("lock")

def handle_http_status(status):
    code = HTTPStatus(status)
    if not code.is_success:
        logger.error(code.description)
    return code.is_success  
