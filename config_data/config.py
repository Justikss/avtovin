import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
# RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEAL_CHAT = os.getenv("DEALERS_CHAT")
SUPPORT_NUMBER = os.getenv("SUPPORT_NUMBER")
SUPPORT_TELEGRAM = os.getenv("SUPPORT_TELEGRAM")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)

