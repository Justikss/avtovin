import contextlib
import logging

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


@contextlib.asynccontextmanager
async def ignore_exceptions():
    try:
        yield
    except (TelegramForbiddenError, TelegramBadRequest) as ex:
        logging.info("Игнорирование исключения: %s", ex)
        pass