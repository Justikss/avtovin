from datetime import datetime

from peewee import CharField, BooleanField, BigIntegerField, TextField, DateField, ForeignKeyField, DateTimeField

from database.db_connect import BaseModel

class Seller(BaseModel):
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
    data_registration = DateField(default=datetime.now().strftime('%Y-%m-%d'))

    is_banned = BooleanField(default=False)
    ban_reason = TextField(null=True)
    block_date = DateTimeField(null=True)

    class Meta:
        db_table = 'Продавцы'

