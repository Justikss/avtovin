import importlib
from typing import Union

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, CallbackQuery, Message

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.utils.pagination_heart import Pagination


class BuyerCarsPagination:
    def __init__(self, data, page_size, current_page):
        self.pagination = Pagination(data, page_size, current_page)

    async def get_output_data(self, callback, state, advert_id):
        get_output_string_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config')
        result = []
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        ic(advert_id)
        for advert in advert_id:
            result_string = await get_output_string_module.get_output_string(advert, state=state, callback=callback)
            if result_string:
                current_data_part = {'car_id': advert_id, 'message_text': result_string}
            ic(result_string)
            photo_album = await AdvertRequester.get_photo_album_by_advert_id(advert_id=advert)
            if photo_album and result_string:
                current_data_part['album'] = photo_album

            ic(photo_album)
            if result_string:
                result.append(current_data_part)
                ic(result)
        return result if not len(result) == 1 else result[0]

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
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        choose_hybrid_handlers_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.hybrid_handlers')

        if not operation:
            operation = '+'

        advert_id = await self.pagination.get_page(operation)  # '+' для начальной страницы
        if advert_id:
            ic(advert_id)
            #  # page_data = page_data[0]
            page_data = await self.get_output_data(request, state, advert_id)
            ic(page_data)
            keyboard = await self.get_keyboard(car_id=advert_id, state=state, page_data=page_data)
            # message_text = await get_output_string(page_data)
            # Здесь код для отправки данных текущей страницы
            # page_header, page_footer = await self.get_page(page_data)
            page_footer = {
                'message_text': lexicon_module.LEXICON['sepp']*7 + f'[{str(self.pagination.current_page)}/{str(self.pagination.total_pages)}]' + lexicon_module.LEXICON['sepp']*7 + '\n'
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
            await request.answer(lexicon_module.LEXICON['confirm_from_buyer']['non_data_more'])

    @staticmethod
    async def get_keyboard(state, car_id=None, page_data=None):
        inline_keyboard_creator_module = importlib.import_module('keyboards.inline.kb_creator')
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        async def active_offer_in_inactive():
            if page_data:
                lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
                if lexicon_module.LEXICON['footer_for_output_active_offers']['viewed_status'] in page_data['message_text']:
                    print('TRUBORD')
                    return True

        buttons_lexicon_part = lexicon_module.LEXICON.get('chosen_configuration')
        ic(await state.get_state())
        current_state = str(await state.get_state())
        if (current_state.startswith(('CheckNonConfirmRequestsStates',
                                                   'CheckActiveOffersStates',
                                                   'CheckRecommendationsStates')) and
                current_state != 'CheckActiveOffersStates:show_from_search_config'):

            backward_callback_data = 'return_to_choose_requests_brand'
        else:
            backward_callback_data = False

        button_flag = False

        correct_buttons = {}
        for key, value in buttons_lexicon_part.items():


            if backward_callback_data and key == 'backward_in_carpooling':
                key = backward_callback_data
                value = lexicon_module.LEXICON['backward_name']

            elif key == 'confirm_buy_settings:':
                if str(await state.get_state()).startswith(('CheckActiveOffersStates')):
                    continue
                else:
                    car_id = str(car_id[0])
                    # if not car_id[-1].isdigit():
                    #     car_id = car_id[1:2]
                    key = key + car_id
                    ic(key)

            correct_buttons[key] = value
            if key == 'buyer_car_pagination:+':
                if current_state.startswith('CheckActiveOffers') and not button_flag:
                    if page_data and not await active_offer_in_inactive():
                        ic(lexicon_module.LEXICON['chosen_configuration'])
                        correct_buttons[f'confirm_buy_settings:{str(car_id[0])}'] = lexicon_module.LEXICON['chosen_configuration'][
                            'confirm_buy_settings:']
                        button_flag = True



        keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(
            input_data={'buttons': correct_buttons}, dynamic_buttons=True)
        return keyboard
