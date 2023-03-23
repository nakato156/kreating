from pathlib import Path
from PIL import Image
from io import BytesIO

def save_img(path: Path, file_bytes: bytes) -> bool:
    img = Image.open(BytesIO(file_bytes))

    if img.format != 'PNG':
        img = img.convert('RGBA')

    buffer = BytesIO()
    img.resize((250, 250)).save(buffer, format='PNG')  
    
    buffer.seek(0)
    with open(path, 'wb') as f:
        f.write(buffer.read())

    return True

def resize_img(path: Path, width:int, height:int = None) -> BytesIO:
    if height == None: height = width

    imagen = Image.open(path)
    resized_image = imagen.resize((width, height))
    
    buffer = BytesIO()
    resized_image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def check_email(uni, email:str) -> bool:
    return email.endswith(uni.dominio)