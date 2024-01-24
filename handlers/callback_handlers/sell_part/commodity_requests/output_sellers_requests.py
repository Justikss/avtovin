import traceback
from copy import copy

from aiogram.exceptions import TelegramServerError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message, FSInputFile
from typing import List, Union
import importlib

from database.tables.car_configurations import CarAdvert
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from states.requests_by_seller import SellerRequestsState
from handlers.utils.pagination_heart import Pagination
from utils.get_currency_sum_usd import get_valutes

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')



async def set_car_id_in_redis(callback, output_data_part):
    '''Метод подставляет id машины в коллбэк дату'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    load_data = dict()

    if isinstance(output_data_part, list):
        output_data_part = output_data_part[0]
    ic(output_data_part)
    if output_data_part:
        car_id = output_data_part.get('car_id')
    else:
        return
    if not car_id:
        car_id = output_data_part['message_text'].split('\n')[0].split('№')[-1].split('<')[0]

    load_data['car_id'] = car_id if not isinstance(car_id, CarAdvert) else car_id.id

    offer_id = output_data_part.get('offer_id')
    if offer_id:
        load_data['offer_id'] = offer_id

    ic()
    ic(car_id)
    ic(load_data)
    await message_editor.redis_data.set_data(
        key=f'{str(callback.from_user.id)}:seller_request_data', value=load_data)

car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

async def output_message_constructor(advert_id: int | str | CarAdvert) -> dict:
    '''Создатель строк для вывода зарегистрированных заявок продавца'''
    # lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    if isinstance(advert_id, int | str):
        advert = await car_advert_requests_module\
            .AdvertRequester.get_where_id(advert_id)
        ic()
        ic(advert)
        if not advert:
            return False

    ic(advert)

    if advert.mileage:
        mileage = advert.mileage.name
        year_of_realise = advert.year.name

    else:
        mileage, year_of_realise = None, None
    #     heart = ''
    #
    output_string = f'''{copy(Lexicon_module.LexiconSellerRequests.output_car_request_header).format(
        offer_number=advert.id)}{await create_advert_configuration_block(car_state=advert.state.name, engine_type=advert.complectation.engine.name,
                                                                     brand=advert.complectation.model.brand.name,
                                                                     model=advert.complectation.model.name,
                                                                     complectation=advert.complectation.name, color=advert.color.name,
                                                                     mileage=mileage, year_of_realise=year_of_realise,
                                                                     sum_price=advert.sum_price, usd_price=advert.dollar_price)}'''
    output_string = output_string.format()
    ic(output_string)

    current_photo_album = await car_advert_requests_module\
        .AdvertRequester.get_photo_album_by_advert_id(advert.id)

    if current_photo_album:
        commodity_photo_album = [photo['id'] for photo in current_photo_album]
    else:
        commodity_photo_album = None


    output_data = {'album': commodity_photo_album, 'message_text': output_string}


    return output_data


async def output_sellers_commodity_page(request: Union[CallbackQuery, Message], state: FSMContext, pagination_data=None, output_data_part=None, current_page=None):
    '''процесс вывода существующих заявок продавца'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    inline_keyboard_creator_module = importlib.import_module('keyboards.inline.kb_creator')
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

    ic(output_data_part)
    user_id = str(request.from_user.id)
    if isinstance(request, CallbackQuery):
        message = request.message
    else:
        message = request


    # seller_requests_pagination = await message_editor.redis_data.delete_key(
    #     key=user_id + ':seller_requests_pagination')

    seller_requests_pagination = await message_editor.redis_data.get_data(
        key=user_id + ':seller_requests_pagination', use_json=True)


    if seller_requests_pagination and seller_requests_pagination != 'null':
        seller_requests_pagination = Pagination(**seller_requests_pagination)
    else:
        seller_requests_pagination = Pagination(data=pagination_data,
                                                 page_size=Lexicon_module.LexiconSellerRequests.pagination_pagesize)

        dicted_pagination_class = await seller_requests_pagination.to_dict()

        await message_editor.redis_data.set_data(key=user_id + ':seller_requests_pagination',
                                                 value=dicted_pagination_class)
    ic()
    ic(current_page)
    if current_page:
        seller_requests_pagination.current_page = current_page-1
        ic()
        ic(seller_requests_pagination.current_page)
    if not output_data_part:
        output_data_part = await seller_requests_pagination.get_page(operation='+')

    commodity_card_messages_id = []
    output_part = None
    commodity_card_message = None
    ic(output_data_part)
    current_state = str(await state.get_state())
    for id_value in output_data_part:
        ic(id_value)

        # if isinstance(key, tuple) and key[0] == 'ActiveOffers':
        #     output_part = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(request, key[1], car_id=value)
        ic(current_state)
        if current_state == 'SellerRequestsState:application_review':
            output_part = await output_message_constructor(id_value)
            if isinstance(output_part, list):
                output_part = output_part[0]
            ic(output_part)
            ic()
        elif current_state == 'SellerFeedbacks:review_applications':
            offer_ids = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(request,
                                                                             from_buyer=True,
                                                                             viewed=False,
                                                                             offer_id=id_value)

            output_part = await CheckFeedbacksHandler.create_offer_data(request, offer_ids[0])
        if output_part:
            if output_part.get('album'):
                output_part['album'] = output_part['album'][:5]
                media_group = [InputMediaPhoto(media=photo_id if '/' not in photo_id else FSInputFile(photo_id)) for photo_id in output_part['album'][:-1]]
                media_group.append(InputMediaPhoto(media=output_part['album'][-1] if '/' not in output_part['album'][-1] else FSInputFile(output_part['album'][-1]),
                                                   caption=output_part['message_text']))
                try:
                    commodity_card_message = await message.chat.bot.send_media_group(chat_id=message.chat.id,
                                                                          media=media_group)
                except TelegramServerError:
                    traceback.print_exc()
                    try:
                        commodity_card_message = await message.chat.bot.send_media_group(chat_id=message.chat.id,
                                                                                         media=media_group)
                    except:
                        traceback.print_exc()

                for message in commodity_card_message:
                    commodity_card_messages_id.append(message.message_id)
                commodity_card_message = commodity_card_message[0].message_id
            else:
                commodity_card_message = await message.chat.bot.send_message(chat_id=message.chat.id, text=output_part['message_text'])
                commodity_card_messages_id.append(commodity_card_message.message_id)
                commodity_card_message = commodity_card_message.message_id

        if current_state == 'SellerFeedbacks:review_applications':
            await cached_requests_module.OffersRequester.set_viewed_true(offer_id=output_part['offer_id'])

    await message_editor.redis_data.set_data(key=user_id + ':seller_media_group_messages',
                                             value=commodity_card_messages_id)

    keyboard_part = await message_editor.redis_data.get_data(key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination', use_json=True)

    if keyboard_part['buttons'].get('withdrawn') or keyboard_part['buttons'].get('rewrite_price_by_seller') and output_part:
        ic(output_part)
        await set_car_id_in_redis(request, output_part)

    keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(
        input_data=keyboard_part)

    page_monitoring_string = f'{Lexicon_module.LexiconSellerRequests.page_view_separator}[{seller_requests_pagination.current_page}/{seller_requests_pagination.total_pages}]'
    lexicon_part = {'message_text': page_monitoring_string}

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, my_keyboard=keyboard, delete_mode=True, reply_message=commodity_card_message, save_media_group=True)




async def output_sellers_requests_by_car_brand_handler(request: Union[CallbackQuery, Message], state: FSMContext, chosen_brand=None, current_page=None):
    '''Обработчик кнопки просмотра созданных запросов продавца'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.redis_data.set_data(key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination',
                                             value=Lexicon_module.LexiconSellerRequests.selected_brand_output_buttons)
    if not chosen_brand:

        if isinstance(request, CallbackQuery):
         chosen_brand = request.data.split(':')[1]

        await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':sellers_requests_car_brand_cache',
                                                value=chosen_brand)


    chosen_commodities = await car_advert_requests_module\
        .AdvertRequester.get_by_seller_id_and_brand(seller_id=request.from_user.id, brand=int(chosen_brand))
    ic(chosen_commodities)
    if chosen_commodities:
        chosen_commodities = [advert.id for advert in chosen_commodities]
        await message_editor.redis_data.set_data(
            key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination',
            value=Lexicon_module.LexiconSellerRequests.selected_brand_output_buttons)

        path_after_delete_car = await message_editor.redis_data.get_data(
            key=f'{str(request.from_user.id)}:return_path_after_delete_car')

        if (not path_after_delete_car and not path_after_delete_car.startswith('seller_requests_brand:')) and (isinstance(request, CallbackQuery)):
            await message_editor.redis_data.set_data(
                key=f'{str(request.from_user.id)}:return_path_after_delete_car', value="i'm_sure_delete_feedback")

        await state.set_state(SellerRequestsState.application_review)

        await output_sellers_commodity_page(request, pagination_data=chosen_commodities, state=state, current_page=current_page)

        return True
    else:
        if isinstance(request, CallbackQuery):
            await request.answer(Lexicon_module.LexiconSellerRequests.seller_does_have_active_car_by_brand)
        return False















