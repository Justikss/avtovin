import logging

from utils.lexicon_utils.logging_utils.logg_string_utils import get_user_name

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


__LOGGING_LEXICON = {'reset_tariff_action': 'Обнулил тариф продавцу: ',
                     'set_seller_tariff_action': 'Установил тариф продавцу: ', 'ban_seller': 'Заблокировал продавца: ',
                     'ban_buyer': 'Заблокировал покупателя: ', 'for_reason': '\nПо причине: ', "edit_tariff": 'Редактировал тариф: '}

async def log_admin_action(admin_username, action, subject='', reason=False):
    ic(subject)
    name = await get_user_name(subject)
    if reason:
        reason = f'''{__LOGGING_LEXICON['for_reason']} {reason}'''
    else:
        reason = ''
    logging.info(f"Администратор {admin_username}: {__LOGGING_LEXICON[action]} {name}{reason}")


# log_admin_action(admin_username=, action=)

