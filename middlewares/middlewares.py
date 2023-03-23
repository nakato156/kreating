from flask import session, request, redirect
from functools import wraps

def require_session(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        ruta = request.path[1:]
        if not 'user' in session:
            return redirect(f'/login?redir={ruta}')
        return fun(*args, **kwargs)
    return wrapper

def no_loged_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return redirect('/perfil')
        return fun(*args, **kwargs)
    return wrapper