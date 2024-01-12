import os
from dotenv import load_dotenv, find_dotenv
import logging


logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

logging.basicConfig(level=logging.DEBUG,
                    format='[{asctime}] #{levelname:8} {filename}:'
                            '{lineno} - {name} - {message}',
                    style='{')


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOCATIONIQ_TOKEN = os.getenv("LOCATIONIQ_TOKEN")

ADMIN_CHAT = os.getenv("ADMIN_CHAT")

SUPPORT_NUMBER = os.getenv("SUPPORT_NUMBER")
SUPPORT_NUMBER_2 = os.getenv("SUPPORT_NUMBER_2")
SUPPORT_TELEGRAM = os.getenv("SUPPORT_TELEGRAM")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
MAILING_DATETIME_FORMAT = '%d-%m-%Y %H:%M'
MODIFIED_MAILING_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

REGISTRATION_DATETIME_FORMAT = '%d-%m-%Y'

lifetime_of_redis_record_of_request_caching = 259200
geolocation_cahce_expire = 3600
message_answer_awaited = 3

max_price_len = 20
max_contact_info_len = 100
block_user_reason_text_len = {'max': 256, 'min': 3}
header_message_text: str = f'<b>AUTOWIN</b>\nКарманный Маркет-Плейс\nДля лучших авто.'

money_valute = '$'

faq = '''
<b>Тех поддержка:</b>
Контакты доступны с главного меню по кнопке [Поддержка]
'''

car_configurations_in_keyboard_page = 4

user_pagesize_by_admin = 6
tariffs_pagesize = 6
top_ten_pagesize = 4
admin_brand_pagination_pagesize = 6
faq_seller = '''
\n<b>Продажа:</b>
\nПосле регистрации продавца и подтверждения её от администрации - <b>требуется оформить тариф,
для того чтобы получать отклики:
</b> <i>[Меню продавца] - [Профиль] - [Продлить тариф].</i>\n
<b>Пополнить свою витрину можно через:
</b> <i>[Меню продавца] - [Заявки] - [Создать заявку].</i>
\n<b>Созданные заявки отображаются в:
</b> <i>[Меню продавца] - [Заявки] - [Мои заявки]</i>
Их можно удалить и поменять им цену.\n
<b>Когда пользователь откликается на ваш товар</b> - вам приходит оповещение в чат с ботом, а так же и сам отклик с контактами покупателя в разделе:
<i>[Меню продавца] - [Заявки] - [Мои отклики].</i>
Отклики делятся на просмотренные и новые - соответственно.
\n<b>В разделе откликов, на просмотренные заявки, по необходимости возможно применить команды:</b>
\n<b>Удалить только отклик, с ваших списков, оставив товар на витрине</b>: 
<i>[Просмотренные отклики] - [Сделка сорвалась],</i>
\n<b>Удалить товар вместе с откликом:</b>
<i>[Просмотренные отклики] - [Снять с продажи]</i>
'''
faq_buyer = '''
<b>Покупка:</b>
\nПо прохождению регистрации покупателя - вы можете совершать отклики на подходящие вам автомобили.
\n<b>Поиск машин</b> происходит через цепочку взаимодействия с ботом: 
<i>[Меню покупателя] - [Поиск авто].</i>\n
При поиске автомобилей следует выбирать подходящие вам параметры из предложенных, в итоге вы получите список машин по вашему запросу.
\n<b>Просмотренные, но оставшиеся без вашего подтверждения товары - переходят в раздел:</b>
<i>[Меню покупателя] - [Предложения].</i>
\nОни остаются там до момента отклика с вашей стороны или по истечению 7-ми дней с момента первого просмотра.
'''