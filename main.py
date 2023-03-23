from dotenv import load_dotenv
load_dotenv()

from secrets import token_hex
from flask import Flask
from os import getenv
from routes import public, auth, user_bp, images_bp
from helpers.context_processors import inject_default

app = Flask(__name__)
app.context_processor(inject_default)
app.secret_key = token_hex(16)

app.register_blueprint(public)
app.register_blueprint(auth)
app.register_blueprint(user_bp)
app.register_blueprint(images_bp)

if __name__ == '__main__':
    app.run(debug=getenv('LOCAL'))