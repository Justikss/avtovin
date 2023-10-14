from typing import List, Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, str | int]):
        kbuilder = InlineKeyboardBuilder()
        buttons = list()

        for callback, text in input_data.items():
            if callback != 'message_text' and callback != 'width':
                buttons.append(InlineKeyboardButton(text=text, callback_data=callback))

        width = input_data['width']

        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
