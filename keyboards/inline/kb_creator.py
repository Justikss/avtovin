from typing import List, Dict, Tuple, Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.Lexicon import LEXICON


class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, str | int],
                            button_texts: Set[str] = None, callback_sign: str = None):
        kbuilder = InlineKeyboardBuilder()
        buttons = list()
        width = input_data['width']
        if button_texts:
            backward_is_exists = input_data.get('backward')
            if not backward_is_exists:
                print('NOT')
                backward = {'backward_in_carpooling': input_data.get('backward_in_carpooling')}
            else:
                backward = {'backward': input_data.get('backward')}

            input_data = {callback_sign+text: text for text in button_texts}

            if backward:
                for callback_data, text in backward.items():
                    input_data[callback_data] = text


        for callback, text in input_data.items():
            if callback != 'message_text' and callback != 'width':
                print('PLUS', text)
                buttons.append(InlineKeyboardButton(text=text, callback_data=callback))


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
