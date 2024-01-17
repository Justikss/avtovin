from peewee import CharField

from database.db_connect import BaseModel

class TechSupports(BaseModel):
    link = CharField(unique=True)
    type = CharField(choices=['telegram', 'number'])
    