from flask import render_template
from models import db


def employee_data(app):

    @app.route('/empleados')
    def empleados():
        return render_template('empleados.html')  # Ruta a tu archivo HTML

    # Ruta para obtener los datos de los empleados en formato JSON
    @app.route('/api/empleados', methods=['GET'])
    def get_employees():
        try:
            query = """
                SELECT first_name, last_name, base_salary, document_number, is_active, position
                FROM employee
                JOIN employee_position ON employee.position_id = employee_position.position_id
            """
            result = db.session.execute(text(query))

            empleados = [
                {
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'base_salary': row['base_salary'],
                    'document_number': row['document_number'],
                    'is_active': row['is_active'],
                    'position': row['position']  # Cargo de la persona
                }
                for row in result
            ]

            return jsonify(empleados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500