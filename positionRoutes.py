from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db

def position_data(app):
    
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
    
    
    
    @app.route('/api/cargos/<int:position_id>', methods=['DELETE'])
    def delete_cargo(position_id):
        try:
            print(f"Intentando eliminar cargo con ID: {position_id}")  # Debug

            # Verificar si el cargo existe
            query_check = text("SELECT 1 FROM employee_position WHERE position_id = :id")
            result = db.session.execute(query_check, {'id': position_id}).first()
            if not result:
                return jsonify({'error': 'Cargo no encontrado'}), 404

            # Eliminar el cargo
            query_delete = text("DELETE FROM employee_position WHERE position_id = :id")
            db.session.execute(query_delete, {'id': position_id})
            db.session.commit()

            print("Cargo eliminado con éxito.")  # Debug
            return jsonify({'message': 'Cargo eliminado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error al eliminar el cargo:", str(e))  # Para debug
            return jsonify({'error': str(e)}), 500
        
    

    @app.route('/api/cargos', methods=['POST'])
    def create_cargo():
        try:
            data = request.get_json()
            nombre = data.get('nombre')

            if not nombre:
                return jsonify({'error': 'Nombre del cargo es requerido'}), 400

            query = text("INSERT INTO employee_position (name) VALUES (:nombre)")
            db.session.execute(query, {'nombre': nombre})
            db.session.commit()

            return jsonify({'message': 'Cargo creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el cargo:", str(e))
            return jsonify({'error': str(e)}), 500



    






    


