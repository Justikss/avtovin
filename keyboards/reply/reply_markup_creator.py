from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class CustomReplyKeyboard:
    async def __call__(self, buttons_data: dict):
        """
        Создаёт reply клавиатуру. Каждая кнопка размещается в своем ряду.
        :param buttons_data: Словарь в формате {'Текст кнопки': is_contact_button}, 
                             где is_contact_button - булево значение или None. 
                             Если True, кнопка будет запросом на контакт, если False или None - обычной текстовой кнопкой.
        """
        buttons = []
        for text, is_contact_button in buttons_data.items():
            buttons.append(KeyboardButton(text=text, request_contact=True)
                           if is_contact_button else KeyboardButton(text=text))

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[buttons])

        return keyboard

create_reply_markup = CustomReplyKeyboard()
