#Зарегаешь миддлварь и впишешь это в нужные места.
#Фильтр мешать не должен

import asyncio
from typing import Callable, Any, Awaitable, Union
from aiogram import BaseMiddleware, types, Bot, Dispatcher, F
from aiogram.types import Message

from config_data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(self, handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]], message: types.Message, data: dict[str, Any]) -> Any:
        if not message.media_group_id or not message.photo:
            await handler(message, data)
            return

        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

        data['_is_last'] = True
        data["album"] = self.album_data[message.media_group_id]

        if data.get("_is_last"):
            await handler(message, data)
            if self.album_data.get(message.media_group_id):
                del self.album_data[message.media_group_id]
            del data['_is_last']

dp.message.middleware(AlbumMiddleware())

@dp.message(F.content_type.in_([types.ContentType.PHOTO]))
async def handle_albums(message: types.Message, album: list[types.Message]):
    if message.media_group_id and album[-1].message_id == message.message_id:
        await message.bot.send_photo(chat_id=message.chat.id, photo=album[0].photo[-1].file_id)
        await message.bot.send_photo(chat_id=message.chat.id, photo=album[1].photo[-1].file_id)


async def start():
    await dp.start_polling(bot)
    print('едем')

if __name__ == '__main__':
    asyncio.run(start())
