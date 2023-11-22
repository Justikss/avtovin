from datetime import datetime

from aiogram.types import CallbackQuery
import importlib
from typing import Tuple, Union

from config_data.config import DATETIME_FORMAT
from utils.Lexicon import LexiconSellerProfile
from database.data_requests.person_requests import PersonRequester, Seller
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder

async def get_seller_name(seller_model: Seller) -> Union[Tuple[str, str], str]:
    '''Метод сопоставляющий имя/название продавца/автосалона'''
    if seller_model.dealship_name:
        name = f'{LexiconSellerProfile.dealership_prefix}\n{LexiconSellerProfile.dealership_name_prefix}{seller_model.dealship_name}'
        address = f'{LexiconSellerProfile.dealership_address_prefix}{seller_model.dealship_address}'
        return (name, address)
    else:
        if seller_model.patronymic:
            patronymic = seller_model.patronymic
        else:
            patronymic = ''
        name = f'{LexiconSellerProfile.seller_prefix}{LexiconSellerProfile.seller_name_prefix}{seller_model.name} {seller_model.surname} {patronymic}'

        return name
    

async def seller_profile_card_constructor(callback: CallbackQuery) -> str:
    '''Метод конструирования выводимой карточки профиля'''
    user_id = callback.from_user.id
    seller_tariff_model = TariffToSellerBinder.get_by_seller_id(seller_id=user_id)


    seller_model = PersonRequester.get_user_for_id(user_id=user_id, seller=True)
    seller_model = seller_model[0]
    seller_data = await get_seller_name(seller_model)
    if len(seller_data) == 2:
        seller_data = f'{seller_data[0]}\n{seller_data[1]}'
    else:
        seller_data = f'{seller_data}'
    
    output_string = f'{LexiconSellerProfile.header}{seller_data}\n{LexiconSellerProfile.phonenumber_prefix}{seller_model.phone_number}'

    if seller_tariff_model:
        seller_tariff_model = seller_tariff_model[0]

        if datetime.strptime(seller_tariff_model.end_date_time, DATETIME_FORMAT) < datetime.now():
            output_string += f'\n{LexiconSellerProfile.tarif_expired}'
        else:
            output_string += f'\n{LexiconSellerProfile.tariff_prefix} {seller_tariff_model.tariff.name}\
                {LexiconSellerProfile.tariff_out_date_prefix} {seller_tariff_model.end_date_time}\
                    \n{LexiconSellerProfile.residual_feedback_prefix} {seller_tariff_model.residual_feedback}'

    return output_string

async def output_seller_profile(callback: CallbackQuery):
    '''Обработчик кнопки ПРОФИЛЬ селлера.'''
    message_editor_module = importlib.import_module('handlers.message_editor')
    lexicon_part = {'message_text': await seller_profile_card_constructor(callback=callback),
                    'buttons': LexiconSellerProfile.tariff_extension_button}

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
    await callback.answer()
