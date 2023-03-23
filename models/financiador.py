from peewee import TextField, FloatField, ForeignKeyField, UUIDField
from .base import BaseModel
from .proyecto import Proyecto
from .Users import User
from uuid import uuid4

class Financiador(BaseModel):
    class Meta():
        table_name = 'financiadores'
    
    uuid = UUIDField(primary_key=True, default=uuid4)
    proyecto = ForeignKeyField(Proyecto, backref='financiador')
    usuario = ForeignKeyField(User, backref='financiador')
    descripcion = TextField(null=False)
    porcentaje = FloatField(null=False)
    credito = FloatField()
    interesCredito = FloatField()

Financiador.create_table(safe=True)