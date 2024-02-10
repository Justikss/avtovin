import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import OutputObject

message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт


class TravelMessageEditorInit(OutputObject):
    def __init__(self, delete_mode=None, send_chat=None, my_keyboard=None,
                 need_media_caption=None, save_media_group=None,
                 reply_message=None, button_texts=None, callback_sign=None, reply_mode=None, lexicon_part=None,
                 bot=None, media_group=None, seller_boot=None,
                 dynamic_buttons=None, lexicon_key=''):
        self.lexicon_key = lexicon_key
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

    async def process(self, request: Message | CallbackQuery, state: FSMContext = None):
        await message_editor.travel_editor.edit_message(request=request, **self.__dict__)