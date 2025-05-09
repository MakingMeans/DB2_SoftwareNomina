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

    @app.route('/api/empleados/<string:document_number>', methods=['PUT'])
    def update_employee(document_number):
        try:
            data = request.get_json()

            # Campos a actualizar
            query_update = text("""
                UPDATE employee SET
                    first_name = :first_name,
                    last_name = :last_name,
                    document_type = :document_type,
                    email = :email,
                    phone = :phone,
                    address = :address,
                    city = :city,
                    health_insurance = :health_insurance,
                    pension_fund = :pension_fund,
                    base_salary = :base_salary,
                    position_id = :position_id,
                    department_id = :department_id
                WHERE document_number = :document_number
            """)

            result = db.session.execute(query_update, {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'document_type': data.get('document_type'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address'),
                'city': data.get('city'),
                'health_insurance': data.get('health_insurance'),
                'pension_fund': data.get('pension_fund'),
                'base_salary': data.get('base_salary'),
                'position_id': data.get('position_id'),
                'department_id': data.get('department_id'),
                'document_number': document_number
            })

            db.session.commit()

            if result.rowcount == 0:
                return jsonify({'error': 'Empleado no encontrado'}), 404

            return jsonify({'message': 'Empleado actualizado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        

    @app.route('/api/departamentos_emp', methods=['GET'])
    def get_departamentos_emp():
        try:
            query = text("SELECT department_id AS id, name FROM department ORDER BY name")
            result = db.session.execute(query).mappings()
            deps = [{"id": row["id"], "name": row["name"]} for row in result]
            return jsonify(deps), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/cargos_emp', methods=['GET'])
    def get_cargos_emp():
        try:
            query = text("SELECT position_id AS id, name FROM employee_position ORDER BY name")
            result = db.session.execute(query).mappings()
            cargos = [{"id": row["id"], "name": row["name"]} for row in result]
            return jsonify(cargos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

