from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def createinlinekeyboard(args, row_width=3, dynamic_buttons=0):
    """
    Создает инлайн-клавиатуру из списка элементов.

    Args:
        args: Элементы клавиатуры.
        row_width: Количество элементов в строке.

    Returns:
        InlineKeyboardMarkup: Созданная клавиатура.
    """

    ic(row_width)
    last_buttons = []
    buttons = []
    buttons_part = []
    kbuilder = InlineKeyboardBuilder()

    for index, arg in enumerate(args):

        if isinstance(arg, tuple):
            ic(arg[1])

            if ic('https://' in arg[1]):
                button = InlineKeyboardButton(text=arg[0], url=arg[1].split()[0])
            else:
                button = InlineKeyboardButton(text=arg[0], callback_data=arg[1])
        else:
            raise TypeError("Неверный тип элемента клавиатуры.")

        if dynamic_buttons and len(args) - index <= dynamic_buttons:
            # if buttons_part:
            last_buttons.append(button)
                # buttons_part = []
            # buttons.append([button])
            continue
        kbuilder.add(button)

        # ic((index) % row_width)
        # buttons_part.append(button)
        #
        # if (index-2) % row_width == 0:
        #     buttons.append(buttons_part)
        #     buttons_part = []


    ic(buttons_part, buttons)

    if buttons_part:
        buttons.append([buttons_part])

    # keyboard = InlineKeyboardMarkup(rowwidth=row_width, inline_keyboard=buttons)
    kbuilder.adjust(3, 2, 2, 2, repeat=True)
    for button in last_buttons:
        kbuilder.row(button)

    return kbuilder.as_markup()
