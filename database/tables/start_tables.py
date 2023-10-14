from peewee import SqliteDatabase, Model, TextField, CharField, IntegerField, ForeignKeyField, AutoField

'''Подключение базы данных SQLite'''
db = SqliteDatabase('db.db')


class BaseModel(Model):
    '''Абстрактный класс для соеднинения таблиц с базой данных'''
    class Meta:
        database = db

