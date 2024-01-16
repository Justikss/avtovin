from copy import copy
from datetime import datetime

from aiogram.types import CallbackQuery
import importlib
from typing import Tuple, Union

# from  import captions


async def get_seller_name(seller_model, get_only_fullname=False, for_admin=False) -> Union[Tuple[str, str], str]:
    '''Метод сопоставляющий имя/название продавца/автосалона'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    ic(seller_model.dealship_name, seller_model.dealship_address)
    if seller_model.dealship_name:
        name = f'''{lexicon_module.LexiconSellerProfile.dealership_prefix}\n{lexicon_module.LexiconSellerProfile.dealership_name_prefix.format(dealership_name=seller_model.dealship_name)}'''
        address = f'''{lexicon_module.LexiconSellerProfile.dealership_address_prefix.format(dealership_address=seller_model.dealship_address)}'''
        if get_only_fullname:
            return seller_model.dealship_name
        else:
            return (name, address)
    else:
        admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')
        if seller_model.patronymic:
            patronymic = seller_model.patronymic
        else:
            patronymic = ''

        fullname = f'{seller_model.surname} {seller_model.name} {patronymic}'
        if for_admin:
            name = f'''{lexicon_module.LexiconSellerProfile.seller_prefix}{admin_lexicon_module.captions['surname_name_patronymic']}{fullname}'''
        else:
            name = f'''{lexicon_module.LexiconSellerProfile.seller_prefix}{lexicon_module.LexiconSellerProfile.seller_name_prefix.format(seller_name=fullname)}'''
        if get_only_fullname:
            return fullname
        else:
            return name

async def get_seller_entity(seller_model):
    if seller_model.dealship_name:
        seller_entity = 'legal'
    else:
        seller_entity = 'natural'

    return  seller_entity

async def seller_profile_card_constructor(callback: CallbackQuery = None, user_id=None, get_part=None, for_admin=False) -> tuple | bool:
    '''Метод конструирования выводимой карточки профиля'''
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    ic()
    if not user_id and callback:
        user_id = callback.from_user.id
    elif isinstance(user_id, str):
        user_id = int(user_id)
    ic(user_id)


    seller_model = await person_requester_module.PersonRequester.get_user_for_id(user_id=user_id, seller=True)
    ic(seller_model)
    if not seller_model:
        return False
    else:
        seller_model = seller_model[0]

    seller_entity = await get_seller_entity(seller_model)

    seller_data = await get_seller_name(seller_model, for_admin=for_admin)
    ic(seller_data)
    if len(seller_data) == 2:
        seller_data = f'{seller_data[0]}\n{seller_data[1]}'
    else:
        seller_data = f'{seller_data}'
    ic(seller_data)
    output_string = f'''{lexicon_module.LexiconSellerProfile.header}{seller_data}\n{lexicon_module.LexiconSellerProfile.phonenumber_prefix.format(phone_number=seller_model.phone_number)}'''

    if get_part == 'top':
        return output_string, seller_entity
    elif get_part == 'bottom':
        ic()
        output_string = ''

    dying_tariff_module = importlib.import_module('database.data_requests.dying_tariff')

    tariff_exists = False

    seller_tariff_model = await tariff_to_seller_binder_module.TariffToSellerBinder.get_by_seller_id(seller_id=user_id)
    dying_tariff = await dying_tariff_module.DyingTariffRequester.get_model_by_user_id(user_id)
    ic(seller_tariff_model)

    if seller_tariff_model and not dying_tariff:
        if isinstance(seller_tariff_model, list):
            seller_tariff_model = seller_tariff_model[0]
        if seller_tariff_model.end_date_time < datetime.now():
            output_string += f'\n\n{lexicon_module.LexiconSellerProfile.tarif_expired}'
        else:
            output_string += f'\n{lexicon_module.LexiconSellerProfile.sep}'
            days_to_end = seller_tariff_model.end_date_time - datetime.now()
            output_string += copy(lexicon_module.LexiconSellerProfile.tariff_block.format(
                tariff_name=seller_tariff_model.tariff.name, days_remaining=days_to_end.days,
                feedbacks_remaining=seller_tariff_model.residual_feedback))
            tariff_exists = True
        ic(output_string)
    if not get_part:
        return output_string
    elif get_part == 'bottom':
        return output_string, tariff_exists


async def output_seller_profile(callback: CallbackQuery):
    '''Обработчик кнопки ПРОФИЛЬ селлера.'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    message_editor_module = importlib.import_module('handlers.message_editor')

    message_text = await seller_profile_card_constructor(callback=callback)

    tariff_button = lexicon_module.LexiconSellerProfile.tariff_extension_button if lexicon_module.LexiconSellerProfile.tariff_prefix.split('>')[1].split(':')[0] in message_text else lexicon_module.LexiconSellerProfile.tariff_store_button
    lexicon_part = {'message_text': message_text,
                    'buttons': {**tariff_button, **lexicon_module.LEXICON['return_main_menu_button'], 'width': lexicon_module.LexiconSellerProfile.width}}

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
    await callback.answer()
