from peewee import CharField, AutoField
from .base import BaseModel

class UniversidadAliada(BaseModel):
    class Meta:
        table_name = 'universidades_alidas'

    id = AutoField(primary_key=True)
    nombre = CharField(unique=True, null=False)
    dominio = CharField(unique=True, null=False)

UniversidadAliada.create_table(safe=True)