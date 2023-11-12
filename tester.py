#Зарегаешь миддлварь и впишешь это в нужные места.
#Фильтр мешать не должен

import asyncio
from typing import Callable, Any, Awaitable, Union, List
from aiogram import BaseMiddleware, types, Bot, Dispatcher, F
from aiogram.types import Message

from config_data.config import BOT_TOKEN



bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

from aiogram.types import Message, InputMediaPhoto

mediagroups = {}


@dp.message(F.photo[-1].file_id.as_("photo_id"), F.media_group_id.as_("album_id"))
async def collect_and_send_mediagroup(message: Message, photo_id: str, album_id: int):
    if album_id in mediagroups:
        mediagroups[album_id].append(photo_id)
        return
    mediagroups[album_id] = [photo_id]
    await asyncio.sleep(0.5)

    new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]
    print(new_album)
    await message.answer_media_group(media=new_album)

import asyncio
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

# from bot.user_topic_context import UserTopicContext

# DEFAULT_DELAY = 0.6
#
# class MediaGroupMiddleware(BaseMiddleware):
#     ALBUM_DATA: Dict[str, List[Message]] = {}
#
#     def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
#         self.delay = delay
#
#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any],
#     ) -> Any:
#         print('a')
#         if not event.media_group_id:
#             return await handler(event, data)
#
#         try:
#             self.ALBUM_DATA[event.media_group_id].append(event)
#             return  # Don't propagate the event
#         except KeyError:
#             self.ALBUM_DATA[event.media_group_id] = [event]
#             await asyncio.sleep(self.delay)
#             data["album"] = self.ALBUM_DATA.pop(event.media_group_id)
#
#         return await handler(event, data)
#
# dp.message.middleware(MediaGroupMiddleware())


# @dp.message(F.content_type.in_([types.ContentType.PHOTO]))
# async def handle_albums(message: types.Message, album: list[types.Message]):
#     if message.media_group_id and album[-1].message_id == message.message_id:
#         await message.bot.send_photo(chat_id=message.chat.id, photo=album[0].photo[-1].file_id)
#         await message.bot.send_photo(chat_id=message.chat.id, photo=album[1].photo[-1].file_id)

async def start():
    await dp.start_polling(bot)
    print('едем')

if __name__ == '__main__':
    asyncio.run(start())
