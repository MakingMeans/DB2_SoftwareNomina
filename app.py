import os

CONFIG_FILE = 'config.py'

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        f.write("""# config.py
DB_HOST = 'localhost'
DB_NAME = 'basededatos'
DB_USER = 'usuario'
DB_PASS = 'contrasena'
DB_PORT = '5432'""")
    print(f"{CONFIG_FILE} fue creado automáticamente con valores por defecto.")
    print("Por favor edita el archivo con tus credenciales reales antes de continuar.")
    exit(1)

from flask import Flask
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy con la app
    db.init_app(app)

    with app.app_context():
        # Crear tablas si no existen
        db.create_all()

    # Importar y registrar las rutas
    from routes import user_data
    user_data(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
