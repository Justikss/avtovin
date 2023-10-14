from typing import Union


from aiogram.types import CallbackQuery, Message

from handlers.message_editor import travel_editor


async def main_menu(request: Union[CallbackQuery, Message]):
    await travel_editor.edit_message(lexicon_key='main_menu', request=request, delete_mode=True)
