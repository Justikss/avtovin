import contextlib
import logging

from aiogram.exceptions import TelegramForbiddenError


@contextlib.asynccontextmanager
async def ignore_exceptions():
    try:
        yield
    except TelegramForbiddenError:
        logging.info("Игнорирование исключения: %s", exc_info=True)
        pass