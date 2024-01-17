from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def createinlinekeyboard(args, row_width=3, dynamic_buttons=0):
    """
    Создает инлайн-клавиатуру из списка элементов.

    Args:
        args: Элементы клавиатуры.
        row_width: Количество элементов в строке.

    Returns:
        InlineKeyboardMarkup: Созданная клавиатура.
    """


    buttons = []
    buttons_part = []

    for index, arg in enumerate(args):

        if isinstance(arg, tuple):
            if 'https://' in arg[1]:
                button = InlineKeyboardButton(text=arg[0], callback_data=arg[1])
            else:
                button = InlineKeyboardButton(text=arg[0], callback_data=arg[1])
        else:
            raise TypeError("Неверный тип элемента клавиатуры.")

        if dynamic_buttons and len(args) - index <= dynamic_buttons:
            if buttons_part:
                buttons.append(buttons_part)
                buttons_part = []
            buttons.append([button])
            continue

        ic(index, index+1 % row_width == 0)
        if index+1 % row_width == 0:
            buttons.append(buttons_part)
            buttons_part = []
        else:
            buttons_part.append(button)


    ic(buttons_part, buttons)
    if not buttons:
        buttons = [buttons_part]
    keyboard = InlineKeyboardMarkup(rowwidth=row_width, inline_keyboard=buttons)

    return keyboard
