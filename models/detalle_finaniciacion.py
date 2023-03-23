from peewee import TextField, UUIDField, FloatField, ForeignKeyField, DateTimeField
from .base import BaseModel
from .proyecto import Proyecto
from uuid import uuid4
from datetime import datetime

class DetalleFinanciamiento(BaseModel):
    class Meta():
        table_name = 'detalles_financiamiento'
    
    uuid = UUIDField(primary_key=True, default=uuid4)
    proyecto = ForeignKeyField(Proyecto, backref='detalles_financiaciones')
    descripcion = TextField(null=False)
    porcentaje = FloatField(null=False)
    credito = FloatField(null=True)
    interesCredito = FloatField(null=True)
    fecha_inscripcion = DateTimeField(default=datetime.now)
    fecha_fin = DateTimeField(default=datetime.now)

DetalleFinanciamiento.create_table(safe=True)