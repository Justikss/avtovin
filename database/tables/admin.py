from datetime import datetime

from peewee import BigIntegerField, DateField, IntegerField

from database.db_connect import BaseModel

class Admin(BaseModel):
    telegram_id = BigIntegerField(primary_key=True, unique=True)
    admin_rang = IntegerField(default=0)
    data_registration = DateField(default=datetime.now().strftime('%d-%m-%Y'))
