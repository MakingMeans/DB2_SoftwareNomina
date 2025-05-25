from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db
from audit import audit_log


def employee_data(app):

    @app.route('/empleados')
    def empleados():

        return render_template(
            'partials/empleados.html')
    
    @app.route('/api/formulario-empleado')
    def get_form_data():
        tipos_documento = [
            {'val': 'CC', 'label': 'Cédula de ciudadanía'},
            {'val': 'CE', 'label': 'Cédula de extranjería'},
            {'val': 'TI', 'label': 'Tarjeta de identidad'},
            {'val': 'PP', 'label': 'Pasaporte'},
            {'val': 'RC', 'label': 'Registro civil'}
        ]

        ciudades = [
            {'val': 'BOG', 'label': 'Bogotá, D.C.'},
            {'val': 'MED', 'label': 'Medellín'},
            {'val': 'CLO', 'label': 'Cali'},
            {'val': 'BAQ', 'label': 'Barranquilla'},
            {'val': 'CTG', 'label': 'Cartagena'},
            {'val': 'CUN', 'label': 'Cúcuta'},
            {'val': 'PEI', 'label': 'Pereira'},
            {'val': 'MZL', 'label': 'Manizales'},
            {'val': 'IBG', 'label': 'Ibagué'}
        ]

        eps_colombia = [
            {'val': 'SURA', 'label': 'EPS SURA'},
            {'val': 'SANITAS', 'label': 'EPS Sanitas'},
            {'val': 'COOMEVA', 'label': 'EPS Coomeva'},
            {'val': 'CAFESALUD', 'label': 'EPS Cafesalud'},
            {'val': 'SALUD_TOTAL', 'label': 'EPS Salud Total'},
            {'val': 'NUEVA_EPS', 'label': 'EPS Nueva EPS'},
            {'val': 'COMPENSAR', 'label': 'EPS Compensar'}
        ]

        fondos_pension = [
            {'val': 'COLPENSIONES', 'label': 'Colpensiones (Público)'},
            {'val': 'PORVENIR', 'label': 'Porvenir'},
            {'val': 'PROTECCION', 'label': 'Protección'},
            {'val': 'COLFONDOS', 'label': 'Colfondos'},
            {'val': 'SKANDIA', 'label': 'Skandia'},
            {'val': 'OLD_MUTUAL', 'label': 'Old Mutual'}
        ]

        # Convertir explícitamente los RowMapping a dict
        departamentos_query = text("SELECT department_id AS id, name FROM department")
        departamentos = db.session.execute(departamentos_query).mappings().all()
        departamentos = [dict(row) for row in departamentos]

        cargos_query = text("SELECT position_id AS id, name FROM employee_position")
        cargos = db.session.execute(cargos_query).mappings().all()
        cargos = [dict(row) for row in cargos]

        return jsonify({
            "tipos_documento": tipos_documento,
            "ciudades": ciudades,
            "eps": eps_colombia,
            "fondos_pension": fondos_pension,
            "departamentos": departamentos,
            "cargos": cargos
        })



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
                ORDER BY document_number
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
            # Obtener el ID del empleado a partir del número de documento
            get_id_query = text("SELECT employee_id FROM employee WHERE document_number = :doc")
            result = db.session.execute(get_id_query, {'doc': document_number}).fetchone()

            if not result:
                return jsonify({'error': 'Empleado no encontrado'}), 404
            
            audit_log(
                action="delete",
                table="employee",
                data_before={
                    "document_number": document_number
                },
            )

            employee_id = result.employee_id

            # Eliminar primero las nóminas relacionadas
            delete_payroll_query = text("DELETE FROM payroll WHERE employee_id = :emp_id")
            db.session.execute(delete_payroll_query, {'emp_id': employee_id})

            # Luego eliminar al empleado
            delete_employee_query = text("DELETE FROM employee WHERE employee_id = :emp_id")
            db.session.execute(delete_employee_query, {'emp_id': employee_id})

            db.session.commit()

            return jsonify({'message': 'Empleado y nóminas asociadas eliminados correctamente'}), 200

        except Exception as e:
            print("Error al eliminar empleado:", e)
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
            audit_log(
                action="insert",
                table="employee",
                data_after={
                    "document_number": document_number
                },
            )

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

            query_select = text("SELECT * FROM employee WHERE document_number = :document_number")
            result = db.session.execute(query_select, {'document_number': document_number})
            current = result.mappings().first()
            if not current:
                return jsonify({'error': 'Empleado no encontrado'}), 404

            current_data = dict(current)
            changes = {}
            for field in [
                'first_name', 'last_name', 'document_type', 'email', 'phone',
                'address', 'city', 'health_insurance', 'pension_fund',
                'base_salary', 'position_id', 'department_id'
            ]:
                if str(data.get(field)) != str(current_data.get(field)):
                    changes[field] = {
                        'before': current_data.get(field),
                        'after': data.get(field)
                    }

            query = text("""
                UPDATE employee
                SET first_name = :first_name,
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

            db.session.execute(query, {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'document_type': data['document_type'],
                'email': data['email'],
                'phone': data['phone'],
                'address': data['address'],
                'city': data['city'],
                'health_insurance': data['health_insurance'],
                'pension_fund': data['pension_fund'],
                'base_salary': data['base_salary'],
                'position_id': data['position_id'],
                'department_id': data['department_id'],
                'document_number': document_number
            })

            db.session.commit()
            if changes:
                audit_log(
                    action="update",
                    table="employee",
                    data_before={"updated_employee": document_number},
                    data_after=changes,
                )
            return jsonify({'message': 'Empleado actualizado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error en update_employee:", e)
            return jsonify({'error': str(e)}), 500


    @app.route('/api/empleado', methods=['GET'])
    def get_employee_by_document():
        try:
            document_number = request.args.get('document_number')

            if not document_number:
                return jsonify({'error': 'Parámetro "document_number" es requerido.'}), 400

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
                WHERE employee.document_number = :document_number
            """

            result = db.session.execute(
                text(query), {'document_number': document_number}
            ).mappings().fetchone()

            if not result:
                return jsonify({'message': 'Empleado no encontrado.'}), 404

            empleado = {
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'base_salary': result['base_salary'],
                'document_number': result['document_number'],
                'is_active': result['is_active'],
                'position': result['position']
            }

            return jsonify(empleado), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
