import importlib
import traceback
from copy import copy
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic

from handlers.callback_handlers.hybrid_part.return_main_menu import return_main_menu_callback_handler
from handlers.utils.pagination_heart import Pagination
from utils.chat_cleaner.media_group_messages import delete_media_groups



class CachedRequestsView:
    '''Сердце класса - output_message_with_inline_pagination'''
    @staticmethod
    async def output_message_with_inline_pagination(callback: CallbackQuery | Message, buttons_data=None, operation=None,
                                                    state: Optional[FSMContext] = None, pagesize=None, current_page=0):
        '''Пока что адаптирован под покупателя(см. get_keyboard)
        Требует контент в виде key: value для кнопок'''
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        redis_key = f'{str(callback.from_user.id)}:inline_buttons_pagination_data'

        if buttons_data:
            if not isinstance(buttons_data, list):
                data = [buttons_data]
            else:
                data = buttons_data
            ic(type(data))
            ic(data, len(data))
            if len(data) == 1:
                data = [{key: value} for key, value in data[0].items()]
            pagination = Pagination(data=data, page_size=pagesize, current_page=current_page)
            operation = '+'
            delete_mode = True
            ic()
        else:
            pagination_data = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
            delete_mode = False
            # ic(pagination_data)
            if pagination_data:
                pagination = Pagination(**pagination_data)
            else:
                return await return_main_menu_callback_handler(callback, state)
        if not operation:
            operation = callback.data.split(':')[-1]

        keyboard = await CachedRequestsView.get_keyboard(callback, pagination, operation, state)
        # ic(await state.get_state())
        try:
            await CachedRequestsView.send_message_with_keyboard(callback, keyboard, pagination, redis_key, state=state,
                                                                delete_mode=delete_mode)
        except Exception as ex:
            traceback.print_exc()
            ic(keyboard, pagination, redis_key)
            ic(ex)
            pass

        if isinstance(callback, CallbackQuery):
            await callback.answer()

    @staticmethod
    async def send_message_with_keyboard(callback, keyboard, pagination, redis_key, state: Optional[FSMContext] = None,
                                         delete_mode=False):
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        if state:
            current_state = str(await state.get_state())
            ic(current_state)
            memory_storage = await state.get_data()
        else:
            current_state = None
            memory_storage = None
        ic(current_state)

        message_text = await CachedRequestsView.action_resources_splitter(redis_module, callback, current_state, memory_storage)
        ic(message_text)
        ic(memory_storage.get('message_text') if memory_storage else None)

        if memory_storage and isinstance(callback, CallbackQuery):
            media_group = await CachedRequestsView.get_media_group(memory_storage, state, callback, delete_mode)
        else:
            media_group = None
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=message_text,
                                                        delete_mode=delete_mode, my_keyboard=keyboard,
                                                        media_group=media_group,
                                                        save_media_group=callback.data.startswith('inline_buttons_pagination:') if isinstance(callback, CallbackQuery) else None)
        # await callback.message.edit_reply_markup(reply_markup=keyboard)
        await redis_module.redis_data.set_data(key=redis_key, value=await pagination.to_dict())
        ic()


    @staticmethod
    async def action_resources_splitter(redis_module, callback, current_state, memory_storage):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        sub_text = True
        message_text = None

        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')

        if user_state == 'buy' and current_state:
            if current_state.startswith('CheckNonConfirmRequestsStates'):
                message_text = lexicon_module.LEXICON['cached_requests_for_buyer_message_text']
            elif current_state.startswith('CheckActiveOffersStates'):
                message_text = lexicon_module.LEXICON['active_offers_for_buyer_message_text']
            elif current_state.startswith('CheckRecommendationsStates'):
                message_text = lexicon_module.LEXICON['recommended_offers_for_buyer_message_text']
            else:
                message_text = {'message_text': memory_storage.get('message_text')}
                sub_text = False
            if message_text and sub_text:
                message_text['message_text'] = f'''{message_text['message_text']}{lexicon_module.LEXICON['make_choose_brand']}'''
        elif user_state == 'sell':
            if memory_storage:
                message_text = memory_storage.get('message_text')
            if not message_text:
                message_text = lexicon_module.LexiconSellerRequests.select_brand_message_text
        elif user_state == 'admin':
            # if current_state:
            if memory_storage:
                message_text = {'message_text': memory_storage.get('message_text')}

        return message_text

    @staticmethod
    async def get_media_group(memory_storage, state, callback, delete_mode):
        media_group = memory_storage.get('media_group_for_inline_pg')
        media_group_in_chat = memory_storage.get('media_group_in_chat')

        if media_group_in_chat and not callback.data.startswith('inline_buttons_pagination:'):
            await state.update_data(media_group_in_chat=False)
            await delete_media_groups(callback)
        if media_group:
            # ic(media_group_for_inline_pg=None)
            await state.update_data(media_group_for_inline_pg=None)
            await state.update_data(media_group_in_chat=True)

        return media_group

    @staticmethod
    async def get_keyboard(callback, pagination, operation, state: Optional[FSMContext]):
        inline_creator_module = importlib.import_module('handlers.callback_handlers.buy_part.language_callback_handler')
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        backward_command = None
        dynamic_buttons = 1
        width_value = 2

        if state:
            current_state = await state.get_state()
            memory_storage = await state.get_data()
            ic(memory_storage.get('last_buttons'))
            
            if memory_storage.get('width'):
                width_value = memory_storage.get('width')
                ic(width_value)
                ic()
            if memory_storage.get('dynamic_buttons'):
                dynamic_buttons = memory_storage.get('dynamic_buttons')
        else:
            memory_storage = None
            current_state = None
        user_state = await redis_module.redis_data.get_data(str(callback.from_user.id) + ':user_state')
        if user_state == 'buy':
            backward_command = lexicon_module.LEXICON['backward_from_buyer_offers']
        elif user_state == 'sell':
            if memory_storage:
                ic()
                backward_command = memory_storage.get('last_buttons')
            else:
                backward_command = None
            if not backward_command:
                ic()
                backward_command = lexicon_module.LexiconSellerRequests.keyboard_end_part


        elif user_state == 'admin':
            backward_command = memory_storage.get('backward_command')

        current_page = await pagination.get_page(operation)

        page_count_button = lexicon_module.LEXICON['output_inline_brands_pagination']['page_count'].replace('C',
                                                                                             str(pagination.current_page))
        page_count_button = page_count_button.replace('M', str(pagination.total_pages))
        pagination_interface_buttons = lexicon_module.LEXICON['output_inline_brands_pagination']
        pagination_interface_buttons['page_count'] = page_count_button
        # ic(pagination_interface_buttons, backward_command)


        if isinstance(current_page, list):
            current_page = {key: value for data_part in current_page for key, value in data_part.items()}
        ic(current_page)
        if current_page:
            ic(len(current_page))
            width_value = width_value if len(current_page) >= 2 else 1
            # ic([len(caption) for caption in current_page])
            # max_text_width = max([len(caption) for callback_data, caption in current_page.items()])
            # ic(max_text_width)
            # if max_text_width > 14:
            #     width_value = 1
            width = ({width_value: len(current_page)}, 3, 1, 1)

        if current_state:
            if 'ChooseStates' in current_state:
                Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
                ic()
                # ic(list(current_page.items())[-2:])
                backward_command = Lexicon_module.LastButtonsInCarpooling.last_buttons
                dynamic_buttons = memory_storage.get('dynamic_buttons')

        if not backward_command:
            # seller_lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
            backward_command = memory_storage.get('last_buttons')
            ic()
        if memory_storage and memory_storage.get('dynamic_buttons') and dynamic_buttons == 1:
            dynamic_buttons = memory_storage.get('dynamic_buttons')
            ic(backward_command)
            # if 'input_to_load_color' in current_state:
            #     ic(len(current_page))
            #     width = ({width_value: len(current_page)}, 3, 1, 1)

        ic(width)
        ic(current_page, pagination_interface_buttons, backward_command)
        current_buttons = {
            'buttons': {**current_page, **pagination_interface_buttons, **backward_command, 'width': width}}

        # Обновляем сообщение с новой клавиатурой
        ic(current_buttons)
        keyboard = await inline_creator_module.InlineCreator.create_markup(input_data=current_buttons, dynamic_buttons=dynamic_buttons)

        return keyboard

    @staticmethod
    async def inline_buttons_pagination_vector_handler(callback: CallbackQuery, state: FSMContext):
        operation = callback.data.split(':')[-1]
        await CachedRequestsView.output_message_with_inline_pagination(callback, operation=operation, pagesize=8, state=state)
