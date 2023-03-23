from models import User
from peewee import DoesNotExist
from typing import Union

class UserController:
    @staticmethod
    def get_usuario(uuid: str) -> User:
        return User.get_or_none(User.uuid == uuid)
    
    @staticmethod
    def check_usuario_registrado(email: str) -> Union[User, None]:
        return User.get_or_none(User.email == email)

    def check_login(email:str, pwd:str) -> Union[User, None]:
        return User.get_or_none((User.email == email) & (User.password == pwd))

    @staticmethod
    def actualizar_info_usuario(uuid:str, data: dict) -> tuple[bool, str]:
        try:
            user: User = User.get(User.uuid == uuid)
            user.actualizar_info(**data)
            return True, 'Usuario actualizado correctamente'
        except DoesNotExist:
            return False, 'El usuario no existe'
        except Exception as e:
            return False, ''