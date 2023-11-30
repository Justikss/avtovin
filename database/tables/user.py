from database.db_connect import BaseModel
from peewee import CharField, IntegerField, BigIntegerField

class User(BaseModel):
    '''Таблица пользователей.'''
    telegram_id = BigIntegerField(unique=True, primary_key=True) #Поле для идентефикации. Уникальные значения увеличивающиеся на 1
    username = CharField(unique=True)
    name = CharField(verbose_name='Имя') #поле ограничено символами(название столбца)
    surname = CharField(verbose_name='Фамилия') #поле ограничено символами(возможно нулевое значение, название столбца)
    patronymic = CharField(null=True, verbose_name='Отчество') #поле ограничено символами(возможно нулевое значение, название столбца)
    phone_number = CharField(unique=True) #поле ограничено символами(уникальные записи в таблице)

    class Meta:
        '''Название таблицы'''
        db_table = 'Пользователи'