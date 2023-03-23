from flask import session

def inject_default() -> bool:
    return {
        'sesion_activa': 'user' in session,
        'round': round
    }