import importlib
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Update
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from icecream import ic


from utils.safe_dict_class import current_language


# ic.disable()


class LanguageMiddlewareModule:
    async def __call__(
            self,
            event
    ) -> Any:

        redis_module = importlib.import_module('handlers.default_handlers.start')
        redis_key = f'{str(event.from_user.id)}:language'
        language = None

        if isinstance(event, CallbackQuery) and event.data.startswith('language_') and len(event.data) == 11:
            redis_value = event.data.split('_')
            if len(redis_value) >= 1:
                if redis_value[0] == 'language':
                    redis_value = redis_value[1]
                    await redis_module.redis_data.set_data(key=redis_key, value=redis_value)
                    language = redis_value
        if not language:
            redis_key = redis_key
            language = await redis_module.redis_data.get_data(key=redis_key)
        if not language:
            language = 'ru'  # Или другой язык по умолчанию
        ic('language to set: ', language)

        # Установка текущего языка в контекстную переменную
        token = current_language.set(language)
        ic(token)
        # try:
            # Вызов следующего обработчика в цепочке
        return True