from .start_tables import BaseModel
from peewee import ForeignKeyField, IntegerField
from .commodity import Commodity
from .user import User
from .seller import Seller


class ActiveOffers(BaseModel):
    '''История Предложений'''
    seller = ForeignKeyField(Seller, backref='offer_seller')
    buyer = ForeignKeyField(User, backref='offer_buyer')
    car = ForeignKeyField(Commodity, backref='offer_commodity')

    class Meta:
        db_table = 'История Предложений'


