from typing import List, Dict, Tuple, Set, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.Lexicon import LEXICON


class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, Union[str, int]],
                            button_texts: Set[str] = None, callback_sign: str = None):
        kbuilder = InlineKeyboardBuilder()
        buttons = list()
        print(input_data.keys())
        if 'buttons' in input_data.keys():
            print('shpo')
            input_data = input_data['buttons']
            print(input_data)

        width = input_data['width']
        if button_texts:
            backward_is_exists = input_data.get('backward')
            if not backward_is_exists:
                backward = {'backward_in_carpooling': input_data.get('backward_in_carpooling')}
            else:
                backward = {'backward': input_data.get('backward')}
            input_data = {callback_sign+text: text for text in button_texts}

            if backward:
                for callback_data, text in backward.items():
                    input_data[callback_data] = text



        for callback, text in input_data.items():
            if callback != 'message_text' and callback != 'width':
                buttons.append(InlineKeyboardButton(text=text, callback_data=callback))


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
