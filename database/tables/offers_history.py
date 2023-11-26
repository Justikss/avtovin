from datetime import datetime, timedelta

from .start_tables import BaseModel
from peewee import ForeignKeyField, IntegerField, AutoField, BooleanField, DateField, CharField
from .commodity import Commodity
from .user import User
from .seller import Seller



class ActiveOffers(BaseModel):
    '''История Предложений'''
    car_id = ForeignKeyField(Commodity, backref='active_offers')
    seller_id = ForeignKeyField(Seller, backref='active_offers')
    buyer_id = ForeignKeyField(User, backref='active_offers')
    viewed = BooleanField()


    class Meta:
        db_table = 'История_Предложений'

class CacheBuyerOffers(BaseModel):
    '''Кэширование неподтверждённых заявок'''
    buyer_id = ForeignKeyField(User, backref='buyer')
    car_id = ForeignKeyField(Commodity, backref='car')
    # car_brand = CharField()
    datetime_of_deletion = DateField(default=datetime.now() + timedelta(days=3))

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
