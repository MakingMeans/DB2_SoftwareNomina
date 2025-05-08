from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db

def department_data(app):

   
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
        
    
        
    @app.route('/api/departamentos/<int:department_id>', methods=['DELETE'])
    def delete_department(department_id):
        try:
            print(f"Intentando eliminar departamento con ID: {department_id}")  # Debug

            # Verificar si el departamento existe
            query_check = text("SELECT 1 FROM department WHERE department_id = :id")
            result = db.session.execute(query_check, {'id': department_id}).first()
            if not result:
                return jsonify({'error': 'Departamento no encontrado'}), 404

            # Eliminar el departamento
            query_delete = text("DELETE FROM department WHERE department_id = :id")
            db.session.execute(query_delete, {'id': department_id})
            db.session.commit()

            print("Departamento eliminado con éxito.")  # Debug
            return jsonify({'message': 'Departamento eliminado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error al eliminar el departamento:", str(e))  # Para debug
            return jsonify({'error': str(e)}), 500
    @app.route('/api/departamentos', methods=['POST'])
    def create_department():
        try:
            data = request.get_json()
            name = data.get('name')

            if not name:
                return jsonify({'error': 'El nombre es obligatorio'}), 400

            query_insert = text("INSERT INTO department (name) VALUES (:name)")
            db.session.execute(query_insert, {'name': name})
            db.session.commit()

            print(f"Departamento '{name}' creado exitosamente.")
            return jsonify({'message': 'Departamento creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el departamento:", str(e))
            return jsonify({'error': str(e)}), 500
        
    # Ruta para la página de conceptos
    @app.route('/conceptos')
    def conceptos():
        return render_template('partials/conceptos.html')  # Asegúrate de crear esta vista

    # Ruta para obtener los conceptos en formato JSON
    @app.route('/api/conceptos', methods=['GET'])
    def get_conceptos():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre,
                    concept_type AS tipo,
                    description AS descripcion,
                    percentage AS porcentaje,
                    fixed_value AS valor_fijo
                FROM payroll_concept
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'tipo': row['tipo'],
                    'descripcion': row['descripcion'],
                    'porcentaje': row['porcentaje'],
                    'valor_fijo': row['valor_fijo']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Ruta para la página HTML de periodos
    @app.route('/periodos')
    def periodos():
        return render_template('partials/payroll_period.html')

    # API para obtener periodos en formato JSON
    @app.route('/api/periodos', methods=['GET'])
    def get_periodos():
        try:
            query = """
                SELECT 
                    pp.payroll_period_id AS id,
                    pt.description AS tipo_nomina,
                    pp.payroll_date AS fecha
                FROM payroll_period pp
                JOIN payroll_type pt ON pp.payroll_type_id = pt.payroll_type_id
            """
            result = db.session.execute(text(query)).mappings()

            periodos = [
                {
                    'id': row['id'],
                    'tipo_nomina': row['tipo_nomina'],
                    'fecha': row['fecha'].strftime('%Y-%m-%d')
                }
                for row in result
            ]

            return jsonify(periodos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    
    
    


