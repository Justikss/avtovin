from .start_tables import BaseModel
from peewee import ForeignKeyField, IntegerField, AutoField
from .commodity import Commodity
from .user import User
from .seller import Seller



class ActiveOffers(BaseModel):
    '''История Предложений'''
    # offer_id = AutoField(primary_key=True)
    seller = ForeignKeyField(Seller, backref='seller')
    buyer = ForeignKeyField(User, backref='buyer')
    # cars = ForeignKeyField(ActiveOffersToCars, backref='cars')

    class Meta:
        db_table = 'История_Предложений'


class ActiveOffersToCars(BaseModel):
    car_id = ForeignKeyField(Commodity, backref='car_id')
    offer_id = ForeignKeyField(ActiveOffers, backref='offer_id')

    class Meta:
        db_table = 'Связь_предложений_с_машинами'
        indexes = (
            (('car_id', 'offer_id'))
        )
