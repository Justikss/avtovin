import importlib
from copy import copy
from aiogram.types import Message, CallbackQuery
from icecream import ic
from handlers.utils.pagination_heart import Pagination
from utils.Lexicon import LEXICON, LexiconCommodityLoader, LexiconSellerRequests


class CachedRequestsView:
    '''Сердце класса - choose_brand_for_output'''
    @staticmethod
    async def choose_brand_for_output(callback: CallbackQuery, car_brands=None, operation=None):
        '''Пока что адаптирован под покупателя(см. get_keyboard)
        Требует контент в виде key: value для кнопок'''
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        redis_key = f'{str(callback.from_user.id)}:inline_buttons_pagination_data'

        if car_brands:
            # inline_buttons_data = copy(LexiconCommodityLoader.load_commodity_brand['buttons'])
            # inline_buttons_data =
            # ic(inline_buttons_data)
            # ic(car_brands)
            # if isinstance(car_brands, dict):
            #     data = [{key: value for key, value in inline_buttons_data.items() if value in car_brands.values()}]
            # else:
            #     data = [{key: value for key, value in inline_buttons_data.items() if value in car_brands}]
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

        try:
            await CachedRequestsView.send_message_with_keyboard(callback, keyboard, pagination, redis_key)
        except:
            pass

        await callback.answer()

    @staticmethod
    async def send_message_with_keyboard(callback, keyboard, pagination, redis_key):
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')
        if user_state == 'buy':
            message_text = LEXICON['cached_requests_for_buyer_message_text']
        elif user_state == 'sell':
            message_text = LexiconSellerRequests.select_brand_message_text

        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=message_text,
                                                        delete_mode=True, my_keyboard=keyboard)
        # await callback.message.edit_reply_markup(reply_markup=keyboard)
        await redis_module.redis_data.set_data(key=redis_key, value=await pagination.to_dict())

    @staticmethod
    async def get_keyboard(callback, pagination, operation):
        inline_creator_module = importlib.import_module('handlers.callback_handlers.buy_part.language_callback_handler')
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')
        if user_state == 'buy':
            backward_command = LEXICON['return_main_menu_only']
        elif user_state == 'sell':
            backward_command = LexiconSellerRequests.keyboard_end_part

        page_count_button = LEXICON['output_inline_brands_pagination']['page_count'].replace('C',
                                                                                             str(pagination.current_page))
        page_count_button = page_count_button.replace('M', str(pagination.total_pages))
        pagination_interface_buttons = LEXICON['output_inline_brands_pagination']
        pagination_interface_buttons['page_count'] = page_count_button
        ic(pagination_interface_buttons, backward_command)
        current_page = await pagination.get_page(operation)
        ic(current_page)
        current_buttons = {
            'buttons': {**backward_command, **pagination_interface_buttons, **current_page[0], 'width': (-1, -3, -2)}}
        # Обновляем сообщение с новой клавиатурой
        keyboard = await inline_creator_module.InlineCreator.create_markup(input_data=current_buttons)

        return keyboard

    @staticmethod
    async def inline_buttons_pagination_vector_handler(callback: CallbackQuery):
        operation = callback.data.split(':')[-1]
        await CachedRequestsView.choose_brand_for_output(callback, operation=operation)
