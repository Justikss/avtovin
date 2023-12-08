import importlib
import traceback
from copy import copy
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic
from handlers.utils.pagination_heart import Pagination


class CachedRequestsView:
    '''Сердце класса - choose_brand_for_output'''
    @staticmethod
    async def choose_brand_for_output(callback: CallbackQuery, car_brands=None, operation=None, state: Optional[FSMContext] = None):
        '''Пока что адаптирован под покупателя(см. get_keyboard)
        Требует контент в виде key: value для кнопок'''
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        redis_key = f'{str(callback.from_user.id)}:inline_buttons_pagination_data'

        if car_brands:
            data = [car_brands]
            ic(type(data))
            ic(data)
            pagination = Pagination(data=data, page_size=8, current_page=1)
            operation = '+'
        else:
            pagination_data = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
            ic(pagination_data)
            pagination = Pagination(**pagination_data)

        if not operation:
            operation = callback.data.split(':')[-1]

        keyboard = await CachedRequestsView.get_keyboard(callback, pagination, operation)
        # ic(await state.get_state())
        try:
            await CachedRequestsView.send_message_with_keyboard(callback, keyboard, pagination, redis_key, state=state)
        except Exception as ex:
            traceback.print_exc()
            ic(keyboard, pagination, redis_key)
            ic(ex)
            pass

        await callback.answer()

    @staticmethod
    async def send_message_with_keyboard(callback, keyboard, pagination, redis_key, state: Optional[FSMContext] = None):
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        if state:
            current_state = str(await state.get_state())
        else:
            current_state = None
        ic(current_state)
        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')
        if user_state == 'buy' and current_state:
            if current_state.startswith('CheckNonConfirmRequestsStates'):
                message_text = lexicon_module.LEXICON['cached_requests_for_buyer_message_text']
            elif current_state.startswith('CheckActiveOffersStates'):
                message_text = lexicon_module.LEXICON['active_offers_for_buyer_message_text']
            elif current_state.startswith('CheckRecommendationsStates'):
                message_text = lexicon_module.LEXICON['recommended_offers_for_buyer_message_text']
            else:
                message_text = None
            if message_text:
                message_text['message_text'] = f'''{message_text['message_text']}{lexicon_module.LEXICON['make_choose_brand']}'''
        elif user_state == 'sell':
            message_text = lexicon_module.LexiconSellerRequests.select_brand_message_text

        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=message_text,
                                                        delete_mode=True, my_keyboard=keyboard)
        # await callback.message.edit_reply_markup(reply_markup=keyboard)
        await redis_module.redis_data.set_data(key=redis_key, value=await pagination.to_dict())

    @staticmethod
    async def get_keyboard(callback, pagination, operation):
        inline_creator_module = importlib.import_module('handlers.callback_handlers.buy_part.language_callback_handler')
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')
        if user_state == 'buy':
            backward_command = lexicon_module.LEXICON['backward_from_buyer_offers']
        elif user_state == 'sell':
            backward_command = lexicon_module.LexiconSellerRequests.keyboard_end_part

        page_count_button = lexicon_module.LEXICON['output_inline_brands_pagination']['page_count'].replace('C',
                                                                                             str(pagination.current_page))
        page_count_button = page_count_button.replace('M', str(pagination.total_pages))
        pagination_interface_buttons = lexicon_module.LEXICON['output_inline_brands_pagination']
        pagination_interface_buttons['page_count'] = page_count_button
        ic(pagination_interface_buttons, backward_command)
        current_page = await pagination.get_page(operation)
        ic(current_page)
        current_buttons = {
            'buttons': {**current_page[0], **pagination_interface_buttons, **backward_command, 'width': ({2: len(current_page[0])}, 3, 1)}}
        # Обновляем сообщение с новой клавиатурой
        ic(current_buttons)
        keyboard = await inline_creator_module.InlineCreator.create_markup(input_data=current_buttons)

        return keyboard

    @staticmethod
    async def inline_buttons_pagination_vector_handler(callback: CallbackQuery):
        operation = callback.data.split(':')[-1]
        await CachedRequestsView.choose_brand_for_output(callback, operation=operation)
