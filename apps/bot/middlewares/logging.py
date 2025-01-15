from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Update, User
from aiogram import BaseMiddleware

from loguru import logger


EVENT_FROM_USER = 'event_from_user'


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')

        logger.info(f"User -- {user}")
        return await handler(event, data)


__all__ = [
    'LoggingMiddleware'
]