from flask import Blueprint, render_template, session, request
from middlewares.middlewares import no_loged_required
from controllers import ProjectController, SubscriptionsCtrl, DetalleFinanceCtrl, UniversidadCtrl

public = Blueprint('public_bp', __name__)

@public.get('/')
def index():
    return render_template('index.html')

@public.get('/registro')
@no_loged_required
def view_registro():
    return render_template('registro.html', universidades = UniversidadCtrl.get_universidades())

@public.get('/login')
@no_loged_required
def view_login():
    return render_template('login.html')

@public.get('/proyecto/<string:id>')
def view_proyecto(id):
    proyecto = ProjectController.get_proyecto(id)
    participantes = ProjectController.get_particpantes(proyecto)
    esta_autorizado = ProjectController.check_fundador(proyecto, session['user']['uuid']) if 'user' in session else False

    kwargs = {
        'proyecto': proyecto,
        'eventos': proyecto.eventos,
        'financiacion': DetalleFinanceCtrl.get_financiamiento_actual(proyecto),
        'esta_autorizado': esta_autorizado,
        'participantes': participantes,
        'data': { 'participantes':[], 'porcentajes': [] }
    }
    return render_template('proyecto.html', **kwargs)

@public.get('/proyectos')
def view_proyectos():
    page_number = 1
    page_size = 10
    proyectos = ProjectController.get_proyectos_pub(page_number, page_size, True)
    return render_template('proyectos.html', proyectos=proyectos)

@public.get('/subscribirse')
def subscribirse():
    data:dict = request.json
    email = data.get('email')
    if not email: return {'error': 'Proporcione un email'}
    SubscriptionsCtrl.add_subscripcion(email)
    return {'msg': 'Se ha suscrito!'}