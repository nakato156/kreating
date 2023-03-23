from peewee import CharField, UUIDField, DateTimeField
from datetime import datetime
from .base import BaseModel
from uuid import uuid4

class Subscripcion(BaseModel):
    class Meta:
        table_name = 'subscripciones'

    uuid = UUIDField(primary_key=True, default=uuid4)
    email = CharField(null=False)
    fecha: datetime = DateTimeField(default=datetime.now)

Subscripcion.create_table(safe=True)