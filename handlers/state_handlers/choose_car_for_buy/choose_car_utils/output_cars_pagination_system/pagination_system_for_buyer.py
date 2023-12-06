import importlib
from typing import Union

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, CallbackQuery, Message

from handlers.utils.pagination_heart import Pagination
from utils import Lexicon
from utils.Lexicon import LEXICON


class BuyerCarsPagination:
    def __init__(self, data, page_size, current_page):
        self.pagination = Pagination(data, page_size, current_page)

    async def try_delete_last_media_group(self, request):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        media_group_message = await message_editor.redis_data.get_data(
            key=str(request.from_user.id) + ':last_media_group', use_json=True)
        if media_group_message:
            for message_id in media_group_message:
                try:
                    await request.bot.delete_message(chat_id=request.message.chat.id, message_id=message_id)
                except:
                    pass

            await message_editor.redis_data.delete_key(key=str(request.from_user.id) + ':last_media_group')

    async def send_page(self, request: Union[Message, CallbackQuery], state: FSMContext, operation: str = None):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        if not operation:
            operation = '+'

        page_data = await self.pagination.get_page(operation)  # '+' для начальной страницы
        if page_data:
            page_data = page_data[0]
            keyboard = await self.get_keyboard(car_id=page_data.get('car_id'), state=state)
            # Здесь код для отправки данных текущей страницы
            # page_header, page_footer = await self.get_page(page_data)
            page_footer = {
                'message_text': '-'*10 + f'[{str(self.pagination.current_page)}/{str(self.pagination.total_pages)}]' + '-'*10 + '\n'
            }
            ic()
            await self.try_delete_last_media_group(request)
            if page_data.get('album'):
                delete_mode=False
                await message_editor.travel_editor.edit_message(request=request, lexicon_key='', media_group=page_data.get('album'), lexicon_part=page_data, need_media_caption=True)
            else:
                delete_mode=True
                page_footer['message_text'] += page_data['message_text']
            await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=page_footer, save_media_group=True, my_keyboard=keyboard, delete_mode=delete_mode)

            await message_editor.redis_data.set_data(key=f'{str(request.from_user.id)}:buyer_cars_pagination',
                                                     value=await self.pagination.to_dict())

        else:
            await request.answer(LEXICON['confirm_from_buyer']['non_data_more'])

    @staticmethod
    async def get_keyboard(state, car_id=None):
        inline_keyboard_creator_module = importlib.import_module('keyboards.inline.kb_creator')

        buttons_lexicon_part = LEXICON.get('chosen_configuration')
        ic(await state.get_state())
        current_state = str(await state.get_state())
        if (current_state.startswith(('CheckNonConfirmRequestsStates',
                                                   'CheckActiveOffersStates',
                                                   'CheckRecommendationsStates')) and
                current_state != 'CheckActiveOffersStates:show_from_search_config'):

            backward_callback_data = 'return_to_choose_requests_brand'
        else:
            backward_callback_data = False

        correct_buttons = {}
        for key, value in buttons_lexicon_part.items():
            if backward_callback_data and key == 'backward_in_carpooling':
                key = backward_callback_data

            elif key == 'confirm_buy_settings:':
                if str(await state.get_state()).startswith(('CheckActiveOffersStates')):
                    continue
                else:
                    key = key + str(car_id)
                    ic(key)

            correct_buttons[key] = value


        keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(
            input_data={'buttons': correct_buttons}, dynamic_buttons=True)
        return keyboard

    # async def get_page(self, page_data) -> tuple:
    #     page_data = page_data[0]
    #     message_text = page_data.get('message_text')
    #     photo_album = page_data.get('album')
    #     # Первая фотография с текстом
    #     media = [InputMediaPhoto(media=photo.get('id'), caption=message_text if index == 0 else None)
    #              for index, photo in enumerate(photo_album)]
    #
    #     lexicon_part = {'message_text': LEXICON['confirm_from_buyer']['separator'], 'buttons': LEXICON.get('chosen_configuration')}
    #
    #     return media, lexicon_part

