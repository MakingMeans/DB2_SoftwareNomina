import os

CONFIG_FILE = 'config.py'

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        f.write("""# config.py
DB_HOST = 'localhost'
DB_NAME = 'basededatos'
DB_USER = 'usuario'
DB_PASS = 'contrasena'
DB_PORT = '5432'
MONGO_URI = 'mongodb+srv://user:password@cluster0.xxxxx.mongodb.net""")
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
    from mainRoutes import main_data
    main_data(app)
    from logRoutes import log_data
    log_data(app)
    from employeeRoutes import employee_data
    employee_data(app)
    from positionRoutes import position_data
    position_data(app)
    from departmentRoutes import department_data
    department_data(app)
    from periodsRoutes import periods_data
    periods_data(app)
    from conceptsRoutes import concepts_data
    concepts_data(app)
    from audit import audit_data
    audit_data(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
