import importlib

from aiogram.types import CallbackQuery, Message

from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_inline_pagination import OutputObject

message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт


class TravelMessageEditorInit(OutputObject):
    def __init__(self, lexicon_key, request: Message | CallbackQuery, delete_mode, send_chat, my_keyboard, need_media_caption, save_media_group,
                 reply_message, button_texts, callback_sign, reply_mode, lexicon_part, bot, media_group, seller_boot,
                 dynamic_buttons):
        self.lexicon_key = lexicon_key
        self.request = request
        self.delete_mode = delete_mode
        self.send_chat = send_chat
        self.my_keyboard = my_keyboard
        self.need_media_caption = need_media_caption
        self.save_media_group = save_media_group
        self.reply_message = reply_message
        self.button_texts = button_texts
        self.callback_sign = callback_sign
        self.reply_mode = reply_mode
        self.lexicon_part = lexicon_part
        self.bot = bot
        self.media_group = media_group
        self.seller_boot = seller_boot
        self.dynamic_buttons = dynamic_buttons

    async def process(self):
        await message_editor.travel_editor.edit_message(**self.__dict__)