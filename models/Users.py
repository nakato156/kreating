from peewee import CharField, UUIDField, DateTimeField, IntegerField, ForeignKeyField
from datetime import datetime
from models.universidad import UniversidadAliada
from .base import BaseModel
from uuid import uuid4

class User(BaseModel):
    class Meta:
        table_name = 'usuarios'
    
    uuid:UUIDField = UUIDField(primary_key=True, default=uuid4)
    email = CharField(unique=True, null=False)
    nombres = CharField(null=False)
    telefono = IntegerField(null=False)
    dni = CharField(unique=True, null=False)
    universidad = ForeignKeyField(UniversidadAliada, backref='usuarios', null=False)
    password = CharField(null=False)
    genero = CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')])
    fecha: datetime = DateTimeField(default=datetime.now)

    def actualizar_info(self, telefono, email, universidad):
        self.telefono = telefono
        self.email = email
        self.universidad = universidad
        self.save()

User.create_table(safe=True)