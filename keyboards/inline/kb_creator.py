from typing import List, Dict, Tuple, Set, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.Lexicon import LEXICON


class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, Union[str, int]],
                            button_texts: Set[str] = None, callback_sign: str = None, dynamic_buttons: bool = False):
        kbuilder = InlineKeyboardBuilder()
        buttons = list()
        print(input_data.keys())

        if 'buttons' in input_data.keys():
            print('shpo')
            input_data = input_data['buttons']
        print('indd: ', input_data)

        width = input_data['width']
        
        
            # pre_bottom_index = len(input_data)-2 # -width, last_btn
            # for index, callback_data in enumerate(input_data):
            #     if index < pre_bottom_index:
            #         print(index, pre_bottom_index)
            #         kbuilder.button(text=input_data[callback_data],
            #                         callback_data=callback_data)
            # adjust_width = (width for _ in range(pre_bottom_index // 2))
            # kbuilder.adjust(adjust_width)
            # last_callback_data, last_text = list(input_data)[-2], input_data[list(input_data)[-2]]
            # kbuilder.add(InlineKeyboardButton(text=last_text, callback_data=last_callback_data))
            # return kbuilder.as_markup()

        

        
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

        if dynamic_buttons and width == 2:
            result_format = []
            for index, number in enumerate(buttons[:-1]):
                if index == len(buttons)-2:
                    if len(buttons) % 2 == 0: 
                        result_format.append([number])
                    result_format.append([buttons[index+1]])
                    break

                elif index == 0 or index % 2 == 0:
                    result_format.append([buttons[index], buttons[index+1]])

            return InlineKeyboardMarkup(inline_keyboard=result_format)


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
