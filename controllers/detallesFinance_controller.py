from models import Proyecto, DetalleFinanciamiento
from typing import Union

class DetalleFinanceCtrl():
    @staticmethod
    def crear(proyecto:Proyecto, descripcion, porcentaje, credito, interesCredito) -> DetalleFinanciamiento:
        return DetalleFinanciamiento.create(
            proyecto=proyecto,
            descripcion=descripcion,
            porcentaje=porcentaje,
            credito=credito,
            interesCredito=interesCredito
        )

    @staticmethod
    def get_financiamiento_actual(proyecto: Proyecto) -> Union[DetalleFinanciamiento, None]:
        detalles_financiamiento = proyecto.detalles_financiaciones
        return detalles_financiamiento.order_by(DetalleFinanciamiento.fecha_inscripcion.desc()).first()
