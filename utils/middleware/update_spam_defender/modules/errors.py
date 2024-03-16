import importlib
import logging
import traceback
from typing import Any

from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery

from handlers.utils.message_answer_without_callback import send_message_answer


class ErrorHandler:
    async def __call__(self,
            event,
            exception
    ) -> Any:
        # Обработка исключения
        if isinstance(event, CallbackQuery):
            if event.data.startswith('confirm_buy_settings:'):
                Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
                await send_message_answer(event, Lexicon_module.LEXICON['success_notification'])
                return

        await self.logging_exception(exception, event)



    async def logging_exception(self, exception: Exception, event):
        if isinstance(exception, TelegramAPIError):
            message = exception.message
        else:
            message = ''
        username = event.from_user.username
        user_id = event.from_user.id

        logging.error("Произошла ошибка у %s - %d: %s\n%s\n%s\n%s\n%s\n" + '-' * 25, username, user_id,
                      traceback.format_stack(),
                      exception, message, await self.format_traceback(), exception.args if exception.args else '')

    async def format_traceback(self):
        tb = traceback.format_exc().splitlines()  # Получаем трассировку стека как список строк
        max_length = max(len(line) for line in tb)  # Находим максимальную длину строки
        formatted_tb = ['| ' + line.ljust(max_length) + ' |' for line in tb]  # Добавляем символы '|' с обеих сторон
        return '\n'.join(formatted_tb)  # Выводим результат