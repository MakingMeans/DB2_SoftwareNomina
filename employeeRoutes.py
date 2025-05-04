from flask import render_template, jsonify
from sqlalchemy.sql import text
from models import db


def employee_data(app):

    @app.route('/empleados')
    def empleados():
        return render_template('partials/empleados.html')  # Ruta a tu archivo HTML

    # Ruta para obtener los datos de los empleados en formato JSON
    from sqlalchemy import text  # asegúrate de tener esto arriba

    @app.route('/api/empleados', methods=['GET'])
    def get_employees():
        try:
            query = """
                SELECT 
                    first_name, 
                    last_name, 
                    base_salary, 
                    document_number, 
                    is_active, 
                    employee_position.name AS position
                FROM employee
                JOIN employee_position ON employee.position_id = employee_position.position_id
            """
            result = db.session.execute(text(query)).mappings()

            empleados = [
                {
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'base_salary': row['base_salary'],
                    'document_number': row['document_number'],
                    'is_active': row['is_active'],
                    'position': row['position']
                }
                for row in result
            ]

            return jsonify(empleados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    # Ruta para la página de cargos
    @app.route('/cargos')
    def cargos():
        return render_template('partials/cargos.html')  # Ruta a tu archivo HTML para cargos

    # Ruta para obtener los cargos en formato JSON
    @app.route('/api/cargos', methods=['GET'])
    def get_cargos():
        try:
            query = """
                SELECT 
                    position_id AS id, 
                    name AS cargo
                FROM employee_position
            """
            result = db.session.execute(text(query)).mappings()

            cargos = [
                {
                    'id': row['id'],
                    'cargo': row['cargo']
                }
                for row in result
            ]

            return jsonify(cargos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Ruta para la página de departamentos
    @app.route('/departamentos')
    def departamentos():
        return render_template('partials/departamentos.html')  # Ruta a tu archivo HTML para departamentos

    # Ruta para obtener los departamentos en formato JSON
    @app.route('/api/departamentos', methods=['GET'])
    def get_departamentos():
        try:
            query = """
                SELECT 
                    department_id AS id, 
                    name AS departamento
                FROM department
            """
            result = db.session.execute(text(query)).mappings()

            departamentos = [
                {
                    'id': row['id'],
                    'departamento': row['departamento']
                }
                for row in result
            ]

            return jsonify(departamentos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


