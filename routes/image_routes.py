from flask import Blueprint, request, send_file
from pathlib import Path
from helpers.funciones import resize_img, BytesIO
import requests

images_bp = Blueprint('images_bp', __name__)

folder_imgs:Path = Path(__file__).parent.parent / 'images'
folder_user_imgs:Path = folder_imgs / 'users'
folder_prj_imgs:Path = folder_imgs / 'proyects'

@images_bp.get('/img/dinamic/<string:tipo>/<string:id>')
def get_img(tipo, id):
    ruta:Path = folder_user_imgs if tipo == 'perfil' else folder_prj_imgs

    width = int(request.args.get('w', '25'))
    path_img = ruta / f'{id}.png'
    if not path_img.exists(): 
        response = requests.get("https://via.placeholder.com/250x250")
        imagen = BytesIO(response.content)
    else:
        imagen = resize_img(path_img, width)
    return send_file(imagen, mimetype='image/png')
