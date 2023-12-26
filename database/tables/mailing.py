
from peewee import TextField, DateTimeField, BooleanField, CharField

from database.db_connect import BaseModel

class Mailing(BaseModel):
    recipients_type = CharField()
    text = TextField()
    scheduled_time = DateTimeField()
    is_sent = BooleanField(default=False)


