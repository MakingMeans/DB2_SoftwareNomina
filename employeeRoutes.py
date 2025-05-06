from flask import render_template, jsonify, request
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
        
    @app.route('/api/empleados/<string:document_number>', methods=['DELETE'])
    def delete_employee(document_number):
        try:
            query = text("DELETE FROM employee WHERE document_number = :doc")
            result = db.session.execute(query, {'doc': document_number})
            db.session.commit()

            if result.rowcount == 0:
                return jsonify({'error': 'Empleado no encontrado'}), 404

            return jsonify({'message': 'Empleado eliminado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
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
    @app.route('/api/empleados', methods=['POST'])
    def create_employee():
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = request.get_json()
            
            # Extraer los campos necesarios
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            document_type = data.get('document_type')
            document_number = data.get('document_number')
            email = data.get('email')
            phone = data.get('phone')
            address = data.get('address')
            city = data.get('city')
            health_insurance = data.get('health_insurance')
            pension_fund = data.get('pension_fund')
            base_salary = data.get('base_salary')
            position_id = data.get('position_id')
            department_id = data.get('department_id')

            # Validación de campos obligatorios
            if not all([first_name, last_name, document_type, document_number, base_salary, position_id, department_id]):
                return jsonify({'error': 'Todos los campos obligatorios deben estar presentes'}), 400

            # Insertar el nuevo empleado en la base de datos
            query_insert = text("""
                INSERT INTO employee (first_name, last_name, document_type, document_number, email, phone, address, 
                                    city, health_insurance, pension_fund, base_salary, position_id, department_id) 
                VALUES (:first_name, :last_name, :document_type, :document_number, :email, :phone, :address, 
                        :city, :health_insurance, :pension_fund, :base_salary, :position_id, :department_id)
            """)
            
            # Ejecutar la consulta de inserción
            db.session.execute(query_insert, {
                'first_name': first_name,
                'last_name': last_name,
                'document_type': document_type,
                'document_number': document_number,
                'email': email,
                'phone': phone,
                'address': address,
                'city': city,
                'health_insurance': health_insurance,
                'pension_fund': pension_fund,
                'base_salary': base_salary,
                'position_id': position_id,
                'department_id': department_id
            })
            
            # Confirmar la transacción
            db.session.commit()

            print(f"Empleado {first_name} {last_name} creado exitosamente.")
            return jsonify({'message': 'Empleado creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el empleado:", str(e))
            return jsonify({'error': str(e)}), 500







    


