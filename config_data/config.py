import os
from dotenv import load_dotenv, find_dotenv
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
# RAPID_API_KEY = os.getenv("RAPID_API_KEY")

DEAL_CHAT = os.getenv("DEALERS_CHAT")
ADMIN_CHAT = os.getenv("ADMIN_CHAT")

SUPPORT_NUMBER = os.getenv("SUPPORT_NUMBER")
SUPPORT_TELEGRAM = os.getenv("SUPPORT_TELEGRAM")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
