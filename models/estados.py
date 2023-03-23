from peewee import CharField, AutoField, UUIDField
from .base import BaseModel
from uuid import uuid4

class TipoVisibilidad(BaseModel):
    class Meta:
        table_name = 'tipo_visibilidad'

    id = AutoField(primary_key=True)
    nombre = CharField(unique=True, null=False)

class TipoEstadoProyecto(BaseModel):
    class Meta:
        table_name = 'tipo_estado_proyecto'
    
    id = UUIDField(primary_key=True, default=uuid4)
    nombre = CharField(unique=True, null=False)

TipoVisibilidad.create_table(safe=True)
TipoEstadoProyecto.create_table(safe=True)