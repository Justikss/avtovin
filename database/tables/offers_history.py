from datetime import datetime, timedelta

from database.db_connect import BaseModel
from peewee import ForeignKeyField, IntegerField, AutoField, BooleanField, DateField, CharField, DateTimeField, \
    CompositeKey, SQL

from .car_configurations import CarAdvert, CarState, CarComplectation, CarEngine, CarMileage, CarColor, CarYear
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


class RecommendationsToBuyer(BaseModel):
    buyer = ForeignKeyField(User, field=User.telegram_id, backref='recommendation_parameters')

    complectation = ForeignKeyField(CarComplectation, backref='recommendations')
    state = ForeignKeyField(CarState, backref='recommendations')
    engine_type = ForeignKeyField(CarEngine, backref='recommendations')

    color = ForeignKeyField(CarColor, backref='recommendations', null=True)
    mileage = ForeignKeyField(CarMileage, backref='recommendations', null=True)
    year = ForeignKeyField(CarYear, backref='recommendations', null=True)

    class Meta:
        db_table = 'Параметры_Рекомендаций'



class RecommendedOffers(BaseModel):
    buyer = ForeignKeyField(User, field=User.telegram_id, backref='recommendations')
    advert = ForeignKeyField(CarAdvert, field=CarAdvert.id)
    parameters = ForeignKeyField(RecommendationsToBuyer, field=RecommendationsToBuyer.id, backref='recommendations_offers')

    class Meta:
        db_table = 'Рекомендации'
        primary_key = CompositeKey('buyer', 'advert')


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
