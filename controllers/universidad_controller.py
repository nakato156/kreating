from models import UniversidadAliada

class UniversidadCtrl:
    @staticmethod
    def get_universidades() -> list[UniversidadAliada]:
        return UniversidadAliada.select()
    
    @staticmethod
    def get_universidad_by_nombre(nombre:str) -> UniversidadAliada:
        return UniversidadAliada.select().where(UniversidadAliada.nombre == nombre.upper()).first()
    
    @staticmethod
    def get_universidad_by_id(id:int) -> UniversidadAliada:
        return UniversidadAliada.select().where(UniversidadAliada.id == id).first()