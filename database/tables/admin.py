from datetime import datetime

from peewee import BigIntegerField, DateField

from config_data.config import REGISTRATION_DATETIME_FORMAT
from database.db_connect import BaseModel

class Admin(BaseModel):
    telegram_id = BigIntegerField(primary_key=True, unique=True)
    data_registration = DateField(default=datetime.now().strftime(REGISTRATION_DATETIME_FORMAT))
