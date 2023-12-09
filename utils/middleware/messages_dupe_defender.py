from typing import Dict, Awaitable, Any, Callable

from aiogram import types
from aiogram import BaseMiddleware
import importlib

class DupeDefenderMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: types.TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.CallbackQuery):

            redis_module = importlib.import_module('utils.redis_for_language')
            user_id = str(event.from_user.id)
            message_stopper = await redis_module.redis_data.get_data(key=f'{user_id}:message_dupe_stopper')
            # await redis_module.redis_data.delete_key(key=f'{user_id}:message_dupe_stopper')

            if not message_stopper:
                await redis_module.redis_data.set_data(key=f'{user_id}:message_dupe_stopper', value=True, expire=3)

                result = await handler(event, data)

                await redis_module.redis_data.delete_key(key=f'{user_id}:message_dupe_stopper')

                return result
            else:
                lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
                await event.answer(lexicon_module.LEXICON['awaiting_process'])
                return
        else:
            return await handler(event, data)