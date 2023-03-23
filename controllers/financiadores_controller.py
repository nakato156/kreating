from models import Proyecto, User, Financiador
from typing import Union

class FinanciadorCtrl():
    @staticmethod
    def addFinanciador(proyecto: Proyecto, user:User, data:dict) -> Union[Financiador, bool]:
        try:
            return Financiador.create(proyecto=proyecto, usuario=user, **data)
        except: return False
