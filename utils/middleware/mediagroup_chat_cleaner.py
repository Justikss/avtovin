import asyncio
import importlib
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware, types


class CleanerMiddleware(BaseMiddleware):


    def __init__(self, latency: Union[int, float] = 0.05):
        self.latency = latency

    async def __call__(self, handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]], request: Union[types.Message, types.CallbackQuery], data: dict[str, Any]) -> Any:

        if isinstance(request, types.CallbackQuery):
            print('MIDDLEWARE: ', request.data, request.data.startswith('rewrite_boot_'))
            if request.data.startswith('rewrite_boot_'):
                print('INCLEANER')
                media_group_delete_module = importlib.import_module(
                    'handlers.callback_handlers.sell_part.seller_main_menu')

                await media_group_delete_module.delete_media_groups(request=request)
        else:
            print("MIDDLEWARE NOPOOT", type(request))

        await handler(request, data)


