from typing import List, Dict, Tuple, Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, str | int],
                            button_texts: Set[str] = None, callback_sign: str = None):
        kbuilder = InlineKeyboardBuilder()
        buttons = list()
        width = input_data['width']
        if button_texts:
            backward_is_exists = input_data.get('backward')

            input_data = {callback_sign+text: text for text in button_texts}

            if backward_is_exists:
                input_data['backward'] = 'Назад'


        for callback, text in input_data.items():
            if callback != 'message_text' and callback != 'width':
                buttons.append(InlineKeyboardButton(text=text, callback_data=callback))


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
