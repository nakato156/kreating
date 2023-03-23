from flask import Blueprint, request, session, jsonify, render_template
from models import Proyecto, Proyecto_usuario, TipoEstadoProyecto, Evento
from peewee import fn, JOIN, Case
from middlewares import require_session
from helpers.funciones import save_img, check_email
from controllers import *
from pathlib import Path
from datetime import datetime
import json

from playhouse.shortcuts import model_to_dict

user_bp = Blueprint('user_bp', __name__)

proyectos_por_pagina = 7
path_imgs_proyectos: Path = Path(__file__).parent.parent / 'images' / 'proyects'
path_imgs_usuarios: Path = path_imgs_proyectos.parent / 'users'

@user_bp.get('/perfil')
@require_session
def perfil():
    user = session['user']
    proyectos = ( Proyecto
                .select(Proyecto.uuid, Proyecto.nombre, Proyecto.descripcion, Proyecto.valuacion, Proyecto.estado_id, Proyecto.fecha, Proyecto.visibilidad_id, fn.COUNT(Proyecto_usuario.id).alias('num_participantes'), fn.COUNT(Case(None, ((Evento.fecha < fn.NOW(), Evento.uuid),), 0)).alias('num_eventos'))
                .join(Proyecto_usuario, JOIN.INNER, on=(Proyecto.uuid == Proyecto_usuario.proyecto_id))
                .switch(Proyecto)
                .join(Evento, JOIN.LEFT_OUTER, on=(Proyecto.uuid == Evento.proyecto_id))
                .where((Proyecto_usuario.usuario_id == user['uuid']) & (Proyecto_usuario.rol == 'fundador'))
                .group_by(Proyecto)
                .paginate(1, proyectos_por_pagina)
    )




    print([proyecto.num_eventos for proyecto in proyectos])
    universidades = UniversidadCtrl.get_universidades()
    return render_template('perfil.html', **user, proyectos=proyectos, universidades=universidades)

@user_bp.get('/crear')
@require_session
def view_crear_proyecto():
    user = session['user']
    return render_template('crear.html', email=user['email'])

@user_bp.post('/crear-proyecto')
@require_session
def crear_proyecto():
    img = request.files.get('imagen')
    if not img:
        return jsonify({'error': 'Se necesita la imagen'}), 400

    data = request.form
    valuacion = data.get('valuacion')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    reparticion = data.get('data')
    financiamiento = data.get('financiamiento')
    
    try:
        valuacion: int = int(valuacion)
        reparticion:dict = json.loads(reparticion)
    except:
        return jsonify({'error': 'Error en la valuación o estado del proyecto'}), 400

    if not all((valuacion, nombre, descripcion, reparticion)):
        return jsonify({'error': 'Error en los datos'}), 400
    
    estado = TipoEstadoProyecto.get_or_none(TipoEstadoProyecto.id == data.get('estado', '1'))
    
    if not estado: return jsonify({'error': 'El estado del proyecto no es válido'}), 400
    
    proyecto_existente = ProjectController.check_nombre_similar(nombre)
    if proyecto_existente:
        return jsonify({'error': 'El nombre ya está en uso'}), 400

    if not 'Yo' in reparticion or sum(reparticion.values()) > 100:
        return jsonify({'error': 'Error en los datos'}), 400
    
    data_financiamiento = None
    if estado.id == '1495a8f0bdc542148bc2a1e9003a8afc' and not financiamiento:
        return jsonify({'error': 'Faltan datos de financiamiento'}), 400
    elif estado.id == '1495a8f0bdc542148bc2a1e9003a8afc':
        info_finance:dict = json.loads(financiamiento)
        descrip_finance:str = info_finance.get('descripcion', '').strip()
        
        try:
            credito = info_finance.get('credito')
            if credito: credito = float(credito)
            interes = info_finance.get('interes')
            if interes: interes = float(interes)
        except:
            return jsonify({'error': 'Error en datos de financiamiento'})
        
        if not descrip_finance or (descrip_finance and (credito and interes )):
            return jsonify({'error': 'Faltan datos de financiamiento'})
        
        data_financiamiento = {
            'descripcion': descrip_finance,
            'porcentaje': info_finance['porcentaje'],
            'credito': credito,
            'interesCredito': interes
        }
        
    proyecto = Proyecto.create(nombre=nombre, descripcion=descripcion, valuacion=valuacion, estado=estado)
    if data_financiamiento:
        data_financiamiento['proyecto'] = proyecto
        DetalleFinanceCtrl.crear(**data_financiamiento)

    current_email = session['user']['email']
    es_unico = len(reparticion) == 1

    for email_user, porcentaje in reparticion.items():
        email = current_email if email_user == 'Yo' else email_user
        ProjectController.nuevoProyectoUsuario(proyecto, porcentaje, email, es_unico)
        
    path = path_imgs_proyectos / f'{proyecto.uuid}.png'
    save_img(path, img.read())

    return {'status': True}

@user_bp.post('/aceptar-oferta')
@require_session
def aceptar_oferta():
    data:dict = request.form.to_dict() or request.json
    proyecto_id = data.get('id')
    
    proyecto = ProjectController.get_proyecto(proyecto_id)
    if not proyecto: return {'error': 'Proyecto no encontrado'}, 400
    
    if data.get('status'):
        detalles = DetalleFinanceCtrl.get_financiamiento_actual(proyecto)
        descripcion = 'Acepta la oferta inicial'
        porcentaje, credito, interes = detalles.porcentaje, detalles.credito, detalles.interesCredito
    else:
        descripcion = data.get('descripcion', '').strip().capitalize()
        
        if not proyecto_id or not descripcion:
            return {'error': 'Error en los datos'}, 400
        
        try:
            porcentaje = float(data.get('porcentaje'))
            credito = float(data.get('credito'))
            interes = float(data.get('interes'))
        except:
            return {'error': 'Error en los datos'}, 400
        
    
    usuario = UserController.get_usuario(session['user']['uuid'])

    data = {
        'descripcion': descripcion,
        'porcentaje': porcentaje,
        'credito': credito,
        'interesCredito': interes
    }
    FinanciadorCtrl.addFinanciador(proyecto=proyecto, user=usuario, data=data)
    return {'msg': 'Se envio la oferta'}

@user_bp.post('/add-evento/<string:proyecto_id>')
@require_session
def add_evento(proyecto_id):
    user = session['user']
    proyecto = ProjectController.get_proyecto(proyecto_id)
    res = ProjectController.check_fundador(proyecto, user['uuid'])

    if not res:
        return jsonify({'error': 'No está autorizado'}), 401
    
    data:dict = request.form.to_dict()

    data = dict(map(lambda v: (v[0], v[1].strip()), data.items()))

    try:
        data['fecha'] = datetime.strptime(data['fecha'], "%Y-%m-%d")
        if data['fecha'] < datetime.now():
            return jsonify({'error': 'La fecha no puede ser menor a la actual'}), 400
    except:
        return jsonify({'error': 'La fecha no es válida'}), 400
    
    if not all(data.values()):
        return jsonify({'error':'todos los campos son obligatorios'}), 400
    
    data['virtual'] = 'enlace' in data
    data['proyecto'] = proyecto
    EventoCtrl.crear(data)
    return {'status': 'test'}
    
@user_bp.put('/actualizar/info')
@require_session
def actualizar_info():
    user:dict = session['user']
    user_uuid = user['uuid']
    
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    universidad = int(request.form.get('universidad', 0))

    if not all((universidad, email, telefono)):
        return jsonify({'error': 'Algunos campos están vacios'}), 400
    

    info_universidad = UniversidadCtrl.get_universidad_by_id(universidad)
    if email != user['email'] or universidad != user['universidad']['id']:
        if not check_email(info_universidad, email):
            return jsonify({'error': 'El correo no concuerda con la universidad'}), 400
    
    data = {
        'email': email,
        'telefono': telefono,
        'universidad': info_universidad
    }
    success, message = UserController.actualizar_info_usuario(user_uuid, data)
    
    img = request.files.get('foto')
    if img:
        path = path_imgs_usuarios / f'{user_uuid}.png'
        save_img(path, img.read())
    
    data['universidad'] = model_to_dict(data['universidad'])
    user.update(data)
    session['user'] = user
    
    return {'success': success, 'msg': message}
