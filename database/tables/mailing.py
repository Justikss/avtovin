from datetime import datetime

from peewee import TextField, DateTimeField, BooleanField, CharField, BigIntegerField, ForeignKeyField
from playhouse.postgres_ext import JSONField, ArrayField

from database.db_connect import BaseModel
from database.tables.seller import Seller
from database.tables.user import User


class Mailing(BaseModel):
    recipients_type = CharField()
    text = TextField(null=True)
    media = JSONField(null=True)
    scheduled_time = DateTimeField()
    is_sent = BooleanField(default=False)


class ViewedMailing(BaseModel):
    message_ids = ArrayField()
    mailing = ForeignKeyField(Mailing, backref='viewed_mailings')
    user_id = BigIntegerField()
    buyer = BooleanField()
    seller = BooleanField()
    send_datetime = DateTimeField(default=datetime.now)
