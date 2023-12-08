from datetime import datetime

from aiogram.types import CallbackQuery
import importlib
from typing import Tuple, Union

from config_data.config import DATETIME_FORMAT
from database.data_requests.person_requests import PersonRequester, Seller
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder


async def get_seller_name(seller_model: Seller) -> Union[Tuple[str, str], str]:
    '''Метод сопоставляющий имя/название продавца/автосалона'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    if seller_model.dealship_name:
        name = f'''{lexicon_module.LexiconSellerProfile.dealership_prefix}\n{lexicon_module.LexiconSellerProfile.dealership_name_prefix.replace('X', seller_model.dealship_name)}'''
        address = f'''{lexicon_module.LexiconSellerProfile.dealership_address_prefix.replace('X', seller_model.dealship_address)}'''
        return (name, address)
    else:
        if seller_model.patronymic:
            patronymic = seller_model.patronymic
        else:
            patronymic = ''

        fullname = f'{seller_model.name} {seller_model.surname} {patronymic}'
        name = f'''{lexicon_module.LexiconSellerProfile.seller_prefix}{lexicon_module.LexiconSellerProfile.seller_name_prefix.replace('X', fullname)}'''

        return name
    

async def seller_profile_card_constructor(callback: CallbackQuery) -> str:
    '''Метод конструирования выводимой карточки профиля'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    user_id = callback.from_user.id
    seller_tariff_model = await TariffToSellerBinder.get_by_seller_id(seller_id=user_id)


    seller_model = await PersonRequester.get_user_for_id(user_id=user_id, seller=True)
    seller_model = seller_model[0]
    seller_data = await get_seller_name(seller_model)
    if len(seller_data) == 2:
        seller_data = f'{seller_data[0]}\n{seller_data[1]}'
    else:
        seller_data = f'{seller_data}'
    
    output_string = f'''{lexicon_module.LexiconSellerProfile.header}{seller_data}\n{lexicon_module.LexiconSellerProfile.phonenumber_prefix.replace('X', seller_model.phone_number)}'''

    if seller_tariff_model:
        seller_tariff_model = seller_tariff_model[0]

        if seller_tariff_model.end_date_time < datetime.now():
            output_string += f'\n{lexicon_module.LexiconSellerProfile.tarif_expired}'
        else:
            output_string += f'''\n{lexicon_module.LexiconSellerProfile.tariff_prefix.replace('X', seller_tariff_model.tariff.name)}\
                {lexicon_module.LexiconSellerProfile.tariff_out_date_prefix.replace('X', str(seller_tariff_model.end_date_time))}\
                    \n{lexicon_module.LexiconSellerProfile.residual_feedback_prefix.replace('X', str(seller_tariff_model.residual_feedback))}'''

    return output_string

async def output_seller_profile(callback: CallbackQuery):
    '''Обработчик кнопки ПРОФИЛЬ селлера.'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    message_editor_module = importlib.import_module('handlers.message_editor')
    message_text = await seller_profile_card_constructor(callback=callback)
    tariff_button = lexicon_module.LexiconSellerProfile.tariff_extension_button if lexicon_module.LexiconSellerProfile.tariff_prefix.split('>')[1] in message_text else lexicon_module.LexiconSellerProfile.tariff_store_button
    lexicon_part = {'message_text': message_text,
                    'buttons': {**tariff_button, **lexicon_module.LEXICON['return_main_menu_button'], 'width': lexicon_module.LexiconSellerProfile.width}}

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
    await callback.answer()
