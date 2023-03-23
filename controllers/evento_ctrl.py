from models import Evento, Proyecto
from datetime import datetime

class EventoCtrl():
    @staticmethod
    def crear(data: dict) -> Evento:
        return Evento.create(**data)
    
    @staticmethod
    def get_eventos_siguientes(proyecto: Proyecto):
        eventos = proyecto.eventos
        return eventos.order_by(Evento.fecha > datetime.now)
