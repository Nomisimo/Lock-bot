# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:02:13 2025

@author: kolja
"""
import logging

from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def unpin_all(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """ Unpin all messages from chat."""
    try:
        await context.bot.unpin_all_chat_messages(chat_id=chat_id)
        logger.info(f"Unpinned all messages in chat {chat_id}.", "bot")
    except Exception as e:
        logger.error(f"Error unpinning messages in chat {chat_id}: {e}")
    