from peewee import CharField, UUIDField, DateField, TextField, BooleanField, ForeignKeyField
from models.proyecto import Proyecto
from .base import BaseModel
from uuid import uuid4

class Evento(BaseModel):
    class Meta:
        table_name = 'eventos'
    
    uuid = UUIDField(primary_key=True, default=uuid4)
    nombre = CharField(null=False)
    fecha = DateField()
    descripcion = TextField(null=False)
    virtual = BooleanField(default=False)
    enlace = CharField(null=True)
    proyecto = ForeignKeyField(Proyecto, backref='eventos')

Evento.create_table(safe=True)