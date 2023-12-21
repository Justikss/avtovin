import logging

from utils.lexicon_utils.logging_utils.logg_string_utils import get_user_name

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


__LOGGING_LEXICON = {'reset_tariff_action': 'Обнулил тариф продавцу: ',
                     'set_seller_tariff_action': 'Установил тариф продавцу: ', 'ban_seller': 'Заблокировал продавца: ',
                     'ban_buyer': 'Заблокировал покупателя: '}

async def log_admin_action(admin_username, action, subject=''):
    ic(subject)
    name = await get_user_name(subject)
    logging.info(f"Администратор {admin_username}: {__LOGGING_LEXICON[action]} {name}")


# log_admin_action(admin_username=, action=)

