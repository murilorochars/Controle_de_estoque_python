from peewee import *
from database import db

class Produto(Model):
    nome = CharField()
    minimo = IntegerField()
    quantidade = IntegerField()

    class Meta:
        database = db

db.connect()


db.create_tables([Produto])
