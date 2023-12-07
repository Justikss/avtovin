import math
from typing import List, Dict, Tuple, Set, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.Lexicon import LEXICON


class InlineCreator:
    @staticmethod
    async def create_keyboard_width_is_tuple(buttons, width_config):
        keyboard = InlineKeyboardBuilder()

        # Индекс для отслеживания текущей кнопки
        current_button_index = 0

        for config in width_config:
            if isinstance(config, dict):
                # Обработка конфигурации в виде словаря
                for buttons_in_row, total_buttons in config.items():
                    rows_needed = math.ceil(total_buttons / buttons_in_row)
                    for _ in range(rows_needed):
                        # Вычисляем, сколько кнопок добавить в текущий ряд
                        buttons_to_add = min(buttons_in_row, total_buttons - current_button_index)
                        row_buttons = buttons[current_button_index:current_button_index + buttons_to_add]
                        keyboard.row(*row_buttons)
                        current_button_index += buttons_to_add
            else:
                # Обработка конфигурации в виде числа (количество кнопок в ряду)
                if current_button_index < len(buttons):
                    row_buttons = buttons[current_button_index:current_button_index + config]
                    keyboard.row(*row_buttons)
                    current_button_index += config

        return keyboard.as_markup()

    @staticmethod
    async def create_markup(input_data: Dict[str, Union[str, int]], get_buttons: bool=False,
                            button_texts: Set[str] = None, callback_sign: str = None, dynamic_buttons: Union[bool, int] = False):
        kbuilder = InlineKeyboardBuilder()

        buttons = list()
        print(input_data.keys())

        if 'buttons' in input_data.keys():
            print('shpo')
            input_data = input_data['buttons']
        print('indd: ', input_data)

        width = input_data['width']
        ic(width)



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

        if get_buttons:
            return buttons
        ic(width)
        if dynamic_buttons and isinstance(width, int):
            if isinstance(dynamic_buttons, bool) and dynamic_buttons:
                dynamic_count = 1  # Если dynamic_buttons True, то одна кнопка внизу будет одиночной
            elif isinstance(dynamic_buttons, int):
                dynamic_count = dynamic_buttons  # Целое число определяет количество одиночных кнопок


            result_format = []
            num_buttons = len(buttons)
            index = 0

            # Добавление кнопок в result_format
            while index < num_buttons - dynamic_count:
                row = buttons[index:min(index + width, num_buttons - dynamic_count)]
                result_format.append(row)
                index += width

            # Обработка оставшихся кнопок
            for i in range(dynamic_count):
                if num_buttons - dynamic_count + i < num_buttons:
                    result_format.append([buttons[num_buttons - dynamic_count + i]])

            return InlineKeyboardMarkup(inline_keyboard=result_format)

        elif not isinstance(width, int):

            return await InlineCreator.create_keyboard_width_is_tuple(buttons, width)


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
