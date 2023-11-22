from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List
import importlib


from database.data_requests.commodity_requests import CommodityRequester
from database.tables.commodity import Commodity
from utils.Lexicon import LexiconSellerRequests as Lexicon
from handlers.utils.pagination_heart import Pagination


async def output_message_constructor(commodity_models: List[Commodity]) -> list:
    '''Создатель строк для вывода зарегистрированных заявок продавца'''
    output_data = []
    for car in commodity_models:
        print('construct_string')
        car: Commodity
        header = Lexicon.output_car_request_header.replace('_', str(car.car_id))

        if car.mileage:
            heart = f'''
                    {Lexicon.commodity_year_of_realise}{car.year_of_release}
                    {Lexicon.commodity_mileage}{car.mileage}
                    {Lexicon.commodity_color}{car.color}
                    '''
        else:
            heart = ''

        body = (f'''{Lexicon.commodity_state}{car.state}\
                    {Lexicon.engine_type}{car.engine_type}\
                    {Lexicon.commodity_brand}{car.brand}\
                    {Lexicon.commodity_model}{car.model}\
                    {Lexicon.commodity_complectation}{car.complectation}\
                    {heart}\
                    {Lexicon.commodity_price}{car.price}\
                    ''')
        current_photo_album = CommodityRequester.get_photo_album_by_car_id(car.car_id)

        if current_photo_album:
            commodity_photo_album = [photo['id'] for photo in current_photo_album]
        else:
            commodity_photo_album = None

        output_string = f'{header}{body}'

        output_data.append({'album': commodity_photo_album, 'text': output_string})

    print('output_string', output_data)
    return output_data


async def output_sellers_commodity_page(callback: CallbackQuery, commodity_models=None, output_data_part=None):
    '''процесс вывода существующих заявок продавца'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    inline_keyboard_creator_module = importlib.import_module('keyboards.inline.kb_creator')

    user_id = str(callback.from_user.id)

    seller_requests_pagination = await message_editor.redis_data.get_data(
        key=user_id + ':seller_requests_pagination', use_json=True)

    print('seller_requests_pagination ', seller_requests_pagination)
    if seller_requests_pagination and seller_requests_pagination != 'null':
        seller_requests_pagination = Pagination(**seller_requests_pagination)
    else:
        seller_requests_pagination = Pagination(data=await output_message_constructor(commodity_models),
                                                 page_size=Lexicon.pagination_pagesize)

        dicted_pagination_class = await seller_requests_pagination.to_dict()
        print('dicted_pagination_class_to_dict ', dicted_pagination_class)
        await message_editor.redis_data.set_data(key=user_id + ':seller_requests_pagination',
                                                 value=dicted_pagination_class)

    if not output_data_part:
        output_data_part = await seller_requests_pagination.get_page(operation='+')

    commodity_card_messages_id = []
    for output_part in output_data_part:
        if output_part.get('album'):
            print('output_part ', output_part)
            media_group = [InputMediaPhoto(media=photo_id) for photo_id in output_part['album'][:-1]]
            media_group.append(InputMediaPhoto(media=output_part['album'][-1],
                                               caption=output_part['text']))
            commodity_card_message = await callback.bot.send_media_group(chat_id=callback.message.chat.id,
                                                                      media=media_group)
            for message in commodity_card_message:
                ic(message)
                commodity_card_messages_id.append(message.message_id)

        else:
            commodity_card_message = await callback.bot.send_message(chat_id=callback.message.chat.id, text=output_part['text'])
            commodity_card_messages_id.append(commodity_card_message.message_id)

    await message_editor.redis_data.set_data(key=user_id + ':seller_media_group_messages',
                                             value=commodity_card_messages_id)

    keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(
        input_data=Lexicon.selected_brand_output_buttons, dynamic_buttons=True)

    page_monitoring_string = f'{Lexicon.page_view_separator}[{seller_requests_pagination.current_page}/{seller_requests_pagination.total_pages}]'
    lexicon_part = {'message_text': page_monitoring_string}

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, my_keyboard=keyboard, delete_mode=True)



async def output_sellers_requests_by_car_brand_handler(callback: CallbackQuery, chosen_brand=None ):
    '''Обработчик кнопки просмотра созданных запросов продавца'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not chosen_brand:
        chosen_brand = callback.data.split(':')[1]
        await message_editor.redis_data.set_data(key=str(callback.from_user.id) + ':sellers_requests_car_brand_cache',
                                                value=chosen_brand)
    print(chosen_brand)
    chosen_commodities = CommodityRequester.get_by_seller_id_and_brand(seller_id=callback.from_user.id, car_brand=chosen_brand)
    if chosen_commodities:
        await output_sellers_commodity_page(callback, chosen_commodities)
        await callback.answer()
    else:
        await callback.answer(Lexicon.seller_does_have_active_car_by_brand)

