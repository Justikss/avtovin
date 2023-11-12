import asyncio
import importlib
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware, types


class CleanerMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.05):
        self.latency = latency

    async def __call__(self, handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]], request: Union[types.Message, types.CallbackQuery], data: dict[str, Any]) -> Any:
        redis_data = importlib.import_module('utils.redis_for_language')

