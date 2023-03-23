from models import Proyecto, Proyecto_usuario, User, DetalleFinanciamiento

class ProjectController():
    @staticmethod
    def get_proyecto(uuid: str) -> Proyecto:
        return Proyecto.select().where(Proyecto.uuid == uuid).first()
    
    @staticmethod
    def get_proyectos_pub(pagina:int, cant:int, paginar:bool=None):
        proyecto = Proyecto.select().where(Proyecto.visibilidad_id == 1)
        if paginar: proyecto = proyecto.paginate(pagina, cant)
        return proyecto

    @staticmethod
    def get_proyecto_by_nombre(nombre: str) -> Proyecto:
        return Proyecto.get_or_none(Proyecto.nombre == nombre)
    
    @staticmethod
    def check_nombre_similar(nombre: str) -> Proyecto:
        return Proyecto.get_or_none(Proyecto.nombre ** f'%{nombre}%')

    @staticmethod
    def get_particpantes(proyecto: Proyecto) -> list[Proyecto_usuario]:
        return (Proyecto_usuario.select(Proyecto_usuario.porcentaje, User.nombres, User.email)
                    .join(User, on=(Proyecto_usuario.usuario == User.uuid))
                    .where(Proyecto_usuario.proyecto == proyecto)
                    .dicts())

    @staticmethod
    def check_fundador(proyecto: Proyecto, id_usuario) -> bool:
        return (Proyecto_usuario
        .select()
        .where((Proyecto_usuario.proyecto == proyecto) & 
                (Proyecto_usuario.usuario == id_usuario) & 
                (Proyecto_usuario.rol.in_(['fundador', 'co-fundador']))).first())
    
    @staticmethod
    def nuevoProyecto(data:dict):
        if 'financiacion' in data:
            info_financiacion = data['financiacion']
        DetalleFinanciamiento().save()
        proyecto = Proyecto.create(**data)
    
    @staticmethod
    def nuevoProyectoUsuario(proyecto: Proyecto, porcentaje:float, email_user:str, es_unico:bool):
        return Proyecto_usuario.create(
            proyecto=proyecto,
            usuario=User.get(User.email == email_user),
            porcentaje=porcentaje,
            rol = 'fundador' if es_unico else 'co-fundador'
        )
    
    @staticmethod
    def buscar_proyecto(nombre:str, estado:int=None):
        if not estado: return Proyecto.select().where(Proyecto.nombre ** f'%{nombre}%')
        return Proyecto.select().where((Proyecto.nombre ** f'%{nombre}%') & (Proyecto.estado == estado))
