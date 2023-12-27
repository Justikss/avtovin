
from peewee import TextField, DateTimeField, BooleanField, CharField
from playhouse.postgres_ext import JSONField

from database.db_connect import BaseModel

class Mailing(BaseModel):
    recipients_type = CharField()
    text = TextField(null=True)
    media = JSONField(null=True)
    scheduled_time = DateTimeField()
    is_sent = BooleanField(default=False)


