import asyncio
import importlib
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware, types
from aiogram.types import Update


# from .start import header_controller

class CleanerModule:
    async def __call__(self,  request) -> Any:

        if isinstance(request, types.CallbackQuery):

            if request.data.startswith('rewrite_boot_'):
                media_group_delete_module = importlib.import_module(
                    'handlers.callback_handlers.sell_part.seller_main_menu')

                await media_group_delete_module.delete_media_groups(request=request)
        else:
            pass