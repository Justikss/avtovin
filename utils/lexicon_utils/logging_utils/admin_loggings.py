import logging

from database.tables.car_configurations import CarAdvert
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from utils.lexicon_utils.logging_utils.logg_string_utils import get_user_name
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


__LOGGING_LEXICON = {'reset_tariff_action': 'Обнулил тариф продавцу: ',
                     'set_seller_tariff_action': 'Установил тариф продавцу: ', 'ban_seller': 'Заблокировал продавца: ',
                     'ban_buyer': 'Заблокировал покупателя: ', 'for_reason': '\nПо причине: ',
                     "edit_tariff": 'Редактировал тариф: ', 'delete_tariff': 'Удалил тариф: ', 'add_tariff': 'Добавил тариф: ',
                     'add_mailing': 'Установил сообщение в рассылку с текстом:', 'in_time': ' В ',
                     'delete_mailing': 'Удалил рассылку с текстом: ', 'published_in_time': 'дата публикации: ',
                     'close_advert': 'Удалил объявление продавца: ',
                     'unban_seller': 'Разблокировал продавца: ',
                     'unban_buyer': 'Разблокировал покупателя: ',
                     'added_param': 'Добавил параметр автомобилей: ',
                     'deleted_param': 'Удалил последний параметр автомобилей по ветке: ',
                     'rewrote_param': 'Редактировал последний параметр автомобилей по ветке: ',
                     'add_param_branch': 'Добавил ветку параметров: ',
                     'rebooted_param_branch_photo': 'Обновил фотографии ветки параметров автомобиля: ',
                     'up_to_red': 'Повысил до красного администратора: ',
                     'unban_person': 'Разблокировал пользователя: ',
                     'set_admin': 'Установил нового администратора: ',
                     'del_red_admin': 'Понизил красного администратора до обычного: ',
                     'del_admin': 'Снял администратора: '}

async def log_admin_action(admin_username, action, subject='', reason=False):
    ic(subject)
    if isinstance(subject, str) and subject.startswith('/') and '@' in subject:
        search = re.search(r'@\w+', subject)
        name = search.group()
    else:
        name = await get_user_name(subject)

        if name:
            if len(name) == 2:
                name = f'\n{name[0]}\n{name[1]}'
    if reason:
        if action == 'add_mailing':
            reason = f'''{__LOGGING_LEXICON['in_time']}{reason}'''
        elif isinstance(reason, tuple) and isinstance(reason[0], CarAdvert):
            reason = f'''\n{await create_advert_configuration_block(advert_id=reason[0], language='ru')}\n{__LOGGING_LEXICON['for_reason']} {reason[1]}'''
        elif action == 'delete_mailing':
            reason = f'''{ __LOGGING_LEXICON['published_in_time']} {reason}'''
        elif action in ('deleted_param'):
            reason = reason
        elif action in ('ban_seller', 'ban_buyer', 'close_advert'):
            reason = f'''{__LOGGING_LEXICON['for_reason']} {reason}'''

    else:
        reason = ''
    logging.info(f"Администратор @{admin_username}: {__LOGGING_LEXICON[action]} {name}{reason}")


# log_admin_action(admin_username=, action=)

