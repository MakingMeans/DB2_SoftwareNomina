from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db
from audit import audit_log

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
            audit_log(
                action="delete",
                table="department",
                data_before={
                    "document_number": department_id
                },
                user="admin"
            )
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
            audit_log(
                action="insert",
                table="department",
                data_after={
                    "department_name": name
                },
                user="admin"
            )

            print(f"Departamento '{name}' creado exitosamente.")
            
            return jsonify({'message': 'Departamento creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el departamento:", str(e))
            return jsonify({'error': str(e)}), 500

    @app.route('/api/departamentos/<int:department_id>', methods=['PUT'])
    def update_departamento(department_id):
        try:
            data = request.get_json()
            nuevo_nombre = data.get('nombre')

            if not nuevo_nombre:
                return jsonify({'error': 'El nombre del departamento es requerido'}), 400
            
            query_select = text("SELECT name FROM department WHERE department_id = :id")
            result = db.session.execute(query_select, {'id': department_id}).mappings().fetchone()

            nombre_anterior = result['name']

            query_update  = text("UPDATE department SET name = :nombre WHERE department_id = :id")
            result = db.session.execute(query_update , {'nombre': nuevo_nombre, 'id': department_id})

            if result.rowcount == 0:
                return jsonify({'error': 'Departamento no encontrado'}), 404

            db.session.commit()

            if nombre_anterior != nuevo_nombre:
                audit_log(
                    action='update',
                    table='department',
                    data_before={'department_id': department_id, 'name': nombre_anterior},
                    data_after={'department_id': department_id, 'name': nuevo_nombre},
                    user='admin'
                )
            return jsonify({'message': 'Departamento actualizado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error al actualizar el departamento:", str(e))
            return jsonify({'error': str(e)}), 500

