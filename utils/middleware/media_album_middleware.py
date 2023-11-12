import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware, types


class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.05):
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

        if message.message_id == self.album_data[message.media_group_id][-1].message_id:
            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]

        if data.get("_is_last"):
            max_len = 0
            max_len_album = []
            for album in self.album_data.values():
                if len(album) > max_len:
                    max_len = len(album)
                    max_len_album = album
            data["album"] = max_len_album
            await handler(message, data)
            if self.album_data.get(message.media_group_id):
                del self.album_data[message.media_group_id]
            del data['_is_last']
