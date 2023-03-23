from models import Subscripcion

class SubscriptionsCtrl:
    @staticmethod
    def add_subscripcion(email:str) -> Subscripcion:
        return Subscripcion.create(email = email)
        
