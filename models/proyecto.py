from peewee import CharField, UUIDField, DateTimeField, TextField, DecimalField, ForeignKeyField
from models.Users import User
from models.estados import TipoEstadoProyecto, TipoVisibilidad
from datetime import datetime
from .base import BaseModel
from uuid import uuid4

class Proyecto(BaseModel):
    class Meta:
        table_name = 'proyectos'

    uuid:UUIDField = UUIDField(primary_key=True, default=uuid4)
    nombre = CharField(null=False)
    descripcion = TextField(null=False)
    valuacion:int = DecimalField(null=False)
    estado = ForeignKeyField(TipoEstadoProyecto, backref='proyectos', null=False)
    fecha: datetime = DateTimeField(default=datetime.now)
    visibilidad = ForeignKeyField(TipoVisibilidad, backref='proyectos', null=False)

class Proyecto_usuario(BaseModel):
    class Meta:
        table_name = 'proyectos_usuarios'
    
    proyecto = ForeignKeyField(Proyecto, backref='usuarios')
    usuario = ForeignKeyField(User, backref='proyectos')
    porcentaje = DecimalField(null=False)
    rol = CharField(null=False)

Proyecto.create_table(safe=True)
Proyecto_usuario.create_table(safe=True)