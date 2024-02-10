import importlib
from datetime import datetime

from peewee import BigIntegerField, CharField, BooleanField, DateField, ForeignKeyField

from tests.tests_database.mock_connect import TestModel

mock_connect_module = importlib.import_module('tests.tests_database.mock_connect')


class Seller(TestModel):
    '''Таблица продавцов(селлеры/автосалоны)'''
    telegram_id = BigIntegerField(primary_key=True, unique=True, verbose_name='Телеграм ID')
    phone_number = CharField(verbose_name='Номера телефонов')
    dealship_name = CharField(unique=True, null=True, verbose_name='Название автосалона')
    entity = CharField(verbose_name='Лицо')
    dealship_address = CharField(null=True, verbose_name='Адрес салона')
    name = CharField(null=True, verbose_name='Имя')  # поле ограничено символами(название столбца)
    surname = CharField(null=True, verbose_name='Фамилия')  # поле ограничено символами(возможно нулевое значение, название столбца)
    patronymic = CharField(null=True, verbose_name='Отчество')
    authorized = BooleanField(verbose_name='Наличие авторизации.')
    data_registration = DateField(default=datetime.now().strftime('%d-%m-%Y'))

    class Meta:
        db_table = 'Продавцы'



class CarColor(TestModel):
    name = CharField(unique=True)


class CarBrand(TestModel):
    name = CharField(unique=True)

class CarModel(TestModel):
    brand = ForeignKeyField(CarBrand, backref='models')
    name = CharField()


class CarEngine(TestModel):
    name = CharField(unique=True)


class CarComplectation(TestModel):
    model = ForeignKeyField(CarModel, backref='complectations')
    engine = ForeignKeyField(CarEngine, backref='complectations')
    name = CharField()

class AdvertParameters(TestModel):
    complectation = ForeignKeyField(CarComplectation, backref='parameters')
    color = ForeignKeyField(CarColor, backref='parameters')


class SellerFeedbacksHistory(TestModel):
    seller_id = ForeignKeyField(Seller, backref='feedbacks_history')
    advert_parameters = ForeignKeyField(AdvertParameters, backref='feedbacks_history', null=True)
    feedback_time = DateField(default=datetime.now().strftime('%d-%m-%Y'))



