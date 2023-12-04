from datetime import datetime, timedelta

from database.db_connect import BaseModel
from peewee import ForeignKeyField, IntegerField, AutoField, BooleanField, DateField, CharField, DateTimeField, \
    CompositeKey

from .car_configurations import CarAdvert
from .user import User
from .seller import Seller




class ActiveOffers(BaseModel):
    '''История Предложений'''
    car_id = ForeignKeyField(CarAdvert, field=CarAdvert.id, backref='active_offers')
    seller_id = ForeignKeyField(Seller, field=Seller.telegram_id, backref='active_offers')
    buyer_id = ForeignKeyField(User, field=User.telegram_id, backref='active_offers')
    viewed = BooleanField()


    class Meta:
        db_table = 'История_Предложений'

class CacheBuyerOffers(BaseModel):
    '''Кэширование неподтверждённых заявок'''
    buyer_id = ForeignKeyField(User, field=User.telegram_id, backref='cached_offers')
    car_id = ForeignKeyField(CarAdvert, field=CarAdvert.id, backref='cached_offers')
    message_text = CharField()
    # car_brand = CharField()
    datetime_of_deletion = DateTimeField(default=datetime.now() + timedelta(days=7))

    class Meta:
        db_table = 'Кэш_Открытых_Заявок'
        primary_key = CompositeKey('buyer_id', 'car_id')

#
# class ActiveOffersToCars(BaseModel):
#     car_id = ForeignKeyField(Commodity, backref='car_id')
#     offer_id = ForeignKeyField(ActiveOffers, backref='offer_id')
#
#     class Meta:
#         db_table = 'Связь_предложений_с_машинами'
#         indexes = (
#             (('car_id', 'offer_id'))
#         )
