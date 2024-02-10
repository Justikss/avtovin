import importlib
import os
from dotenv import load_dotenv, find_dotenv
import logging

from utils.lexicon_utils.lexicon_uz.config_uz import DEFAULT_COMMANDS_UZ, header_message_text_uz
import time

os.environ['TZ'] = 'Asia/Tashkent'
time.tzset()  # Применяет изменения часового пояса (работает только на Unix/Linux)

TEST_MOMENT = False

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

logging.basicConfig(level=logging.DEBUG,
                    format='[{asctime}] #{levelname:8} {filename}:'
                            '{lineno} - {name} - {message}',
                    style='{')
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOCATIONIQ_TOKEN = os.getenv("LOCATIONIQ_TOKEN")
DEVELOPER_TELEGRAM_ID = os.getenv('DEVELOPER_TELEGRAM_ID')
ADMIN_SELLERS_CHAT = os.getenv('ADMIN_SELLERS_CHAT')
ADMIN_ADVERTS_CHAT = os.getenv('ADMIN_ADVERTS_CHAT')


DEFAULT_COMMANDS = (
    ("start", "Запустить бота")#,
    # ("help", "Вывести справку")
)
#
# YANDEX_IAM_TOKEN = os.getenv('YANDEX_IAM_TOKEN')
# YANDEX_folder_id = os.getenv('YANDEX_folder_id')

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
MAILING_DATETIME_FORMAT = '%d-%m-%Y %H:%M'
MODIFIED_MAILING_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

REGISTRATION_DATETIME_FORMAT = '%Y-%m-%d'

lifetime_of_redis_record_of_request_caching = 259200
geolocation_cahce_expire = 3600
message_answer_awaited = 2
spam_block_time = 3
long_term_spam_block_time = 3600
anti_spam_duration = 0.7
mailing_interval = 0.05
tech_support_tg_link_buttons_width = 3

mailing_text_max_len = 270
max_price_len = 20
max_phone_number_len = 25
max_contact_info_len = 150
datetime_input_max_len = 16
duration_time_max_len = 8
max_feedbacks_len = 18
max_advert_parameter_name_len = 150
max_naming_len = 70
max_integer_for_database = 2147483647
max_biginteger_for_database = 9223372036854775807
block_user_reason_text_len = {'max': 256, 'min': 3}
header_message_text = '<b>AUTOWIN</b>\nКарманный Маркет-Плейс\nДля лучших авто.'

money_valute = '$'

car_configurations_in_keyboard_page = 4

user_pagesize_by_admin = 6
tariffs_pagesize = 6
top_ten_pagesize = 4
admin_brand_pagination_pagesize = 6


safe_dict_module = importlib.import_module('utils.safe_dict_class')


DEFAULT_COMMANDS = safe_dict_module.SafeDict({'ru': DEFAULT_COMMANDS,
                             'uz': DEFAULT_COMMANDS_UZ})
header_message_text = safe_dict_module.SafeDict({'ru': {'text': header_message_text},
                                'uz': {'text': header_message_text_uz}})

'''
<b>Тех поддержка:</b>
Контакты доступны с главного меню по кнопке [Поддержка]
'''