from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from typing import List, Union
import importlib

from database.data_requests.car_advert_requests import AdvertRequester
from database.tables.car_configurations import CarAdvert
from utils.Lexicon import LexiconSellerRequests as Lexicon
from handlers.utils.pagination_heart import Pagination



async def set_car_id_in_redis(callback, output_data_part):
    '''Метод подставляет id машины в коллбэк дату'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    load_data = dict()

    if isinstance(output_data_part, list):
        output_data_part = output_data_part[0]
    ic(output_data_part)
    car_id = output_data_part.get('car_id')
    if not car_id:
        car_id = output_data_part['message_text'].split('\n')[0].split('№')[-1]

    load_data['car_id'] = car_id

    offer_id = output_data_part.get('offer_id')
    if offer_id:
        load_data['offer_id'] = offer_id

    ic()
    ic(car_id)
    await redis_module.redis_data.set_data(
        key=f'{str(callback.from_user.id)}:seller_request_data', value=load_data)

async def output_message_constructor(commodity_models: List[CarAdvert]) -> list:
    '''Создатель строк для вывода зарегистрированных заявок продавца'''
    output_data = []
    for car in commodity_models:
        print('construct_string')
        car: CarAdvert
        ic(car)
        header = Lexicon.output_car_request_header.replace('_', str(car.id))

        if car.mileage:
            heart = f'''
                    {Lexicon.commodity_year_of_realise}{car.year.name}\
                    {Lexicon.commodity_mileage}{car.mileage.name}\
                    {Lexicon.commodity_color}{car.color.name}\
                    '''
        else:
            heart = ''
        ic(car.complectation)
        body = (f'''{Lexicon.commodity_state}{car.state.name}\
                    {Lexicon.engine_type}{car.engine_type.name}\
                    {Lexicon.commodity_brand}{car.complectation.model.brand.name}\
                    {Lexicon.commodity_model}{car.complectation.model.name}\
                    {Lexicon.commodity_complectation}{car.complectation.name}\
                    \n{heart.strip()}\
                    {Lexicon.commodity_price}{car.price}\
                    ''')
        current_photo_album = await AdvertRequester.get_photo_album_by_advert_id(car.id)

        if current_photo_album:
            commodity_photo_album = [photo['id'] for photo in current_photo_album]
        else:
            commodity_photo_album = None

        output_string = f'{header}{body}'

        output_data.append({'album': commodity_photo_album, 'message_text': output_string})

    print('output_string', output_data)
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

    seller_requests_pagination = await message_editor.redis_data.get_data(
        key=user_id + ':seller_requests_pagination', use_json=True)

    print('seller_requests_pagination ', seller_requests_pagination)
    if seller_requests_pagination and seller_requests_pagination != 'null':
        seller_requests_pagination = Pagination(**seller_requests_pagination)
    else:
        seller_requests_pagination = Pagination(data=pagination_data,
                                                 page_size=Lexicon.pagination_pagesize)

        dicted_pagination_class = await seller_requests_pagination.to_dict()
        print('dicted_pagination_class_to_dict ', dicted_pagination_class)
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
    commodity_card_message = None
    for output_part in output_data_part:
        ic(output_part)


        if output_part.get('album'):
            print('output_part ', output_part)
            media_group = [InputMediaPhoto(media=photo_id) for photo_id in output_part['album'][:-1]]
            print(output_part)
            media_group.append(InputMediaPhoto(media=output_part['album'][-1],
                                               caption=output_part['message_text']))
            commodity_card_message = await message.chat.bot.send_media_group(chat_id=message.chat.id,
                                                                      media=media_group)
            for message in commodity_card_message:
                ic(message)
                commodity_card_messages_id.append(message.message_id)
            commodity_card_message = commodity_card_message[0].message_id
        else:
            commodity_card_message = await message.chat.bot.send_message(chat_id=message.chat.id, text=output_part['message_text'])
            commodity_card_messages_id.append(commodity_card_message.message_id)
            commodity_card_message = commodity_card_message.message_id

        if await state.get_state() == 'SellerFeedbacks:review':
            await cached_requests_module.OffersRequester.set_viewed_true(offer_id=output_part['offer_id'])

    await message_editor.redis_data.set_data(key=user_id + ':seller_media_group_messages',
                                             value=commodity_card_messages_id)

    keyboard_part = await message_editor.redis_data.get_data(key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination', use_json=True)

    if keyboard_part['buttons'].get('withdrawn') or keyboard_part['buttons'].get('rewrite_price_by_seller'):
        ic(output_data_part)
        await set_car_id_in_redis(request, output_data_part)

    keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(
        input_data=keyboard_part)

    page_monitoring_string = f'{Lexicon.page_view_separator}[{seller_requests_pagination.current_page}/{seller_requests_pagination.total_pages}]'
    lexicon_part = {'message_text': page_monitoring_string}

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, my_keyboard=keyboard, delete_mode=True, reply_message=commodity_card_message, save_media_group=True)




async def output_sellers_requests_by_car_brand_handler(request: Union[CallbackQuery, Message], state: FSMContext, chosen_brand=None, current_page=None):
    '''Обработчик кнопки просмотра созданных запросов продавца'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.redis_data.set_data(key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination', value=Lexicon.selected_brand_output_buttons)
    if not chosen_brand:

        # try:
        if isinstance(request, CallbackQuery):
         chosen_brand = request.data.split(':')[1]
        # except:
        #     chosen_brand = LexiconCommodityLoader.load_commodity_brand['buttons'].get(callback.data)
        await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':sellers_requests_car_brand_cache',
                                                value=chosen_brand)
    print(chosen_brand)

    chosen_commodities = await AdvertRequester.get_by_seller_id_and_brand(seller_id=request.from_user.id, brand=int(chosen_brand))
    ic(chosen_commodities)
    if chosen_commodities:
        await message_editor.redis_data.set_data(
            key=f'{str(request.from_user.id)}:last_keyboard_in_seller_pagination',
            value=Lexicon.selected_brand_output_buttons)

        path_after_delete_car = await message_editor.redis_data.get_data(
            key=f'{str(request.from_user.id)}:return_path_after_delete_car')

        if (not path_after_delete_car or not path_after_delete_car.startswith('seller_requests_brand:')) and (isinstance(request, CallbackQuery)):
            await message_editor.redis_data.set_data(
                key=f'{str(request.from_user.id)}:return_path_after_delete_car', value=request.data)

        await output_sellers_commodity_page(request, pagination_data=await output_message_constructor(chosen_commodities), state=state, current_page=current_page)
        if isinstance(request, CallbackQuery):
            await request.answer()
        return True
    else:
        if isinstance(request, CallbackQuery):
            await request.answer(Lexicon.seller_does_have_active_car_by_brand)
        return False

