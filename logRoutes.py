from flask import render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import AppUser, db
from audit import audit_log

def log_data(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            user_input = request.form['user']
            password_input = request.form['pass']

            user = AppUser.query.filter(
                (AppUser.username == user_input) | (AppUser.email == user_input)
            ).first()

            if user and check_password_hash(user.password_hash, password_input):
                return render_template('main.html', message="Inicio de sesión exitoso", success=True)
            else:
                return render_template('index.html', message="Usuario o contraseña incorrectos", success=False)

        return render_template('index.html')
    
    @app.route('/R')
    def about():
        return render_template('signup.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            document_number = request.form['document_number']
            email = request.form['email']

            hashed_password = generate_password_hash(password)

            new_user = AppUser(
                username=username,
                password_hash=hashed_password,
                document_number=document_number,
                email=email
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                audit_log(
                    action="insert",
                    table="app_user",
                    data_after={
                        "document_number": document_number
                    },
                )

                print("Usuario creado con éxito:", new_user.username)
                return render_template('index.html', message="Usuario creado con éxito", success=True)
            except Exception as e:
                return render_template('signup.html', message="Error al registrar", success=False)

        return render_template('signup.html')