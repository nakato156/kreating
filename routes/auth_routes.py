from flask import Blueprint, request, session, make_response, jsonify
from hashlib import sha256
from models import User
from controllers import UserController, UniversidadCtrl
from helpers.funciones import check_email 
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from middlewares import no_loged_required

auth = Blueprint('auth_bp', __name__)

@auth.post('/login')
@no_loged_required
def login():
    data:dict = request.form

    email = data.get('email')
    pwd = sha256(data.get('password').encode()).hexdigest()

    user = UserController.check_login(email, pwd)
    if not user:
        return jsonify({'error': 'Email o contraseña incorecto'}), 401
    
    session['user'] = model_to_dict(user)
    return {'status': True}

@auth.post('/registro')
@no_loged_required
def registro():
    data:dict = request.json

    email = data.get('email')
    nombres = data.get('nombres')
    dni = data.get('dni')
    universidad = data.get('universidad')
    password = sha256(data.get('password').encode()).hexdigest()
    genero = data.get('genero')
    genero = 'F' if int(genero) == 1 else 'M'

    # Validar los campos requeridos
    if not all((email, nombres, dni, universidad, password, genero)):
        return make_response({'error': 'Faltan campos requeridos'}, 400)

    try:
        universidad = UniversidadCtrl.get_universidad_by_id(int(universidad))
        if not universidad: raise ValueError
    except:
        return {'error': 'Universidad no encontrada'}, 400

    if not check_email(universidad, email):
        return {'error': 'El correo no concuerda con la universidad'}, 400

    try:
        user = User.create(
            email=email,
            nombres=nombres,
            dni=dni,
            universidad=universidad,
            password=password,
            genero=genero
        )
        session['user'] = model_to_dict(user)
    except IntegrityError:
        return make_response({'error':'El email o DNI ya están registrados'}, 400)

    return {"status": True, 'msg': 'Usuario creado exitosamente.'}