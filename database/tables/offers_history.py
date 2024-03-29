import importlib
from datetime import datetime, timedelta

from database.db_connect import BaseModel
from peewee import ForeignKeyField, BooleanField, DateTimeField, CompositeKey, DateField, AutoField

from database.tables.car_configurations import CarAdvert, CarState, CarComplectation, CarEngine, CarMileage, CarColor, CarYear
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User
from database.tables.seller import Seller




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
    id = AutoField(primary_key=True)
    buyer_id = ForeignKeyField(User, field=User.telegram_id, backref='cached_offers')
    car_id = ForeignKeyField(CarAdvert, field=CarAdvert.id, backref='cached_offers')
    # car_brand = CharField()
    datetime_of_deletion = DateTimeField(default=datetime.now() + timedelta(days=7))

    class Meta:
        db_table = 'Кэш_Открытых_Заявок'
        indexes = (
            (('buyer_id', 'car_id'), True),  # Создание уникального индекса для пары buyer и advert
        )


class RecommendationsToBuyer(BaseModel):
    buyer = ForeignKeyField(User, field=User.telegram_id, backref='recommendations_to_buyer')

    parameters = ForeignKeyField(AdvertParameters, backref='recommendations_to_buyer')

    class Meta:
        db_table = 'Параметры_Рекомендаций'

class SellerFeedbacksHistory(BaseModel):
    seller_id = ForeignKeyField(Seller, backref='feedbacks_history')
    advert_parameters = ForeignKeyField(AdvertParameters, backref='feedbacks_history', null=True)
    feedback_time = DateField(default=datetime.now().strftime('%d-%m-%Y'))

class RecommendedOffers(BaseModel):
    id = AutoField(primary_key=True)
    buyer = ForeignKeyField(User, field=User.telegram_id, backref='recommendations')
    advert = ForeignKeyField(CarAdvert, field=CarAdvert.id)
    parameters = ForeignKeyField(RecommendationsToBuyer, field=RecommendationsToBuyer.id, backref='recommendations_offers')
    datetime_of_deletion = DateTimeField(default=datetime.now() + timedelta(days=7))


    class Meta:
        db_table = 'Рекомендации'
        indexes = (
            (('buyer', 'advert'), True),  # Создание уникального индекса для пары buyer и advert
        )

