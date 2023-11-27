from typing import List, Dict, Tuple, Set, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.Lexicon import LEXICON


class InlineCreator:
    @staticmethod
    async def create_markup(input_data: Dict[str, Union[str, int]], get_buttons: bool=False,
                            button_texts: Set[str] = None, callback_sign: str = None, dynamic_buttons: bool = False):
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
        if dynamic_buttons and width == 2:
            ic(dynamic_buttons)
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

        elif not isinstance(width, int):
            if width[0] < 0:
                ic(input_data)
                keyboard = InlineKeyboardBuilder()
                buttons_reversed = buttons[::-1]  # Переворачиваем список кнопок

                for row_size in width:
                    row_size = abs(row_size)  # Преобразуем отрицательные числа
                    row_buttons = []

                    for _ in range(row_size):
                        if buttons_reversed:
                            button = buttons_reversed.pop()
                            row_buttons.append(button)
                        else:
                            break  # Если кнопок нет, прерываем цикл

                    keyboard.row(*row_buttons)

                # Обрабатываем оставшиеся кнопки с использованием последнего числа в width
                last_row_size = abs(width[-1])
                while buttons_reversed:
                    keyboard.row(*(button for button in
                                   buttons_reversed[:last_row_size]))
                    buttons_reversed = buttons_reversed[last_row_size:]

                return keyboard.as_markup()
            else:
                button_index = 0
                structured_buttons = []
                for row_value in width:
                    row_buttons = buttons[button_index:button_index + row_value]
                    structured_buttons.append(row_buttons)
                    button_index += row_value

                return InlineKeyboardMarkup(inline_keyboard=structured_buttons)


        keyboard = kbuilder.row(*buttons, width=width)
        keyboard = keyboard.as_markup()

        return keyboard
