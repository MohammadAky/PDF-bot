"""
Subscriber Management
"""

import json
import logging
from typing import List
from config.settings import SUBSCRIBERS_FILE

logger = logging.getLogger(__name__)


def _load_subscribers() -> List[int]:
    """Load subscribers from file"""
    if not SUBSCRIBERS_FILE.exists():
        return []
    
    try:
        with open(SUBSCRIBERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [int(x) for x in data]
    except Exception as e:
        logger.error(f"Error loading subscribers: {e}")
        return []


def _save_subscribers(subscribers: List[int]) -> None:
    """Save subscribers to file"""
    try:
        SUBSCRIBERS_FILE.parent.mkdir(exist_ok=True)
        with open(SUBSCRIBERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subscribers, f)
    except Exception as e:
        logger.error(f"Error saving subscribers: {e}")


def add_subscriber(user_id: int) -> bool:
    """
    Add a user to subscribers
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True if added, False if already subscribed
    """
    subscribers = _load_subscribers()
    
    if user_id in subscribers:
        return False
    
    subscribers.append(user_id)
    _save_subscribers(subscribers)
    logger.info(f"Added subscriber: {user_id}")
    return True


def remove_subscriber(user_id: int) -> bool:
    """
    Remove a user from subscribers
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True if removed, False if not subscribed
    """
    subscribers = _load_subscribers()
    
    if user_id not in subscribers:
        return False
    
    subscribers = [s for s in subscribers if s != user_id]
    _save_subscribers(subscribers)
    logger.info(f"Removed subscriber: {user_id}")
    return True


def is_subscribed(user_id: int) -> bool:
    """
    Check if user is subscribed
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True if subscribed
    """
    subscribers = _load_subscribers()
    return user_id in subscribers


def list_subscribers() -> List[int]:
    """
    Get list of all subscribers
    
    Returns:
        List of subscriber user IDs
    """
    return _load_subscribers()


def get_subscriber_count() -> int:
    """
    Get total number of subscribers
    
    Returns:
        Number of subscribers
    """
    return len(_load_subscribers())


async def notify_subscribers(bot, text: str) -> int:
    """
    Send notification to all subscribers
    
    Args:
        bot: Telegram bot instance
        text: Message text
        
    Returns:
        Number of successful deliveries
    """
    subscribers = _load_subscribers()
    success_count = 0
    
    for user_id in subscribers:
        try:
            await bot.send_message(chat_id=user_id, text=text)
            success_count += 1
        except Exception as e:
            logger.warning(f"Failed to notify subscriber {user_id}: {e}")
    
    logger.info(f"Notified {success_count}/{len(subscribers)} subscribers")
    return success_count