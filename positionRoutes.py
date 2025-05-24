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
        
    @app.route('/api/cargos/<int:position_id>', methods=['PUT'])
    def update_cargo(position_id):
        try:
            data = request.get_json()
            nuevo_nombre = data.get('nombre')

            if not nuevo_nombre:
                return jsonify({'error': 'El nombre del cargo es requerido'}), 400

            query = text("UPDATE employee_position SET name = :nombre WHERE position_id = :id")
            result = db.session.execute(query, {'nombre': nuevo_nombre, 'id': position_id})
            
            if result.rowcount == 0:
                return jsonify({'error': 'Cargo no encontrado'}), 404

            db.session.commit()
            return jsonify({'message': 'Cargo actualizado correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            print("Error al actualizar el cargo:", str(e))
            return jsonify({'error': str(e)}), 500

    @app.route('/api/payroll', methods=['POST'])
    def crear_payroll():
        try:
            data = request.get_json()
            document_number = data['document_number']
            payroll_period_id = data['payroll_period_id']
            worked_days = data['worked_days']

            # Buscar el employee_id según el número de documento
            employee_query = """
                SELECT employee_id FROM employee
                WHERE document_number = :document_number AND is_active = TRUE
            """
            result = db.session.execute(
                text(employee_query),
                {'document_number': document_number}
            ).fetchone()

            if result is None:
                return jsonify({'error': 'Empleado no encontrado o inactivo'}), 404

            employee_id = result.employee_id

            # Insertar la nómina
            insert_query = """
                INSERT INTO payroll (employee_id, payroll_period_id, worked_days)
                VALUES (:employee_id, :payroll_period_id, :worked_days)
            """
            db.session.execute(
                text(insert_query),
                {
                    'employee_id': employee_id,
                    'payroll_period_id': payroll_period_id,
                    'worked_days': worked_days
                }
            )
            db.session.commit()

            return jsonify({'message': 'Nómina creada correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/payroll-1', methods=['POST'])
    def crear_payroll_1():
        try:
            data = request.get_json()
            document_number = data['document_number']
            payroll_period_id = data['payroll_period_id']
            Day_EH = data['Day_EH']
            Nigth_EH = data['Nigth_EH']
            Fest_EH = data['Fest_EH']
            Dom_EH = data['Dom_EH']

            # Buscar el employee_id según el número de documento
            employee_query = """
                SELECT employee_id FROM employee
                WHERE document_number = :document_number AND is_active = TRUE
            """
            result = db.session.execute(
                text(employee_query),
                {'document_number': document_number}
            ).fetchone()

            if result is None:
                return jsonify({'error': 'Empleado no encontrado o inactivo'}), 404

            employee_id = result.employee_id

            # Insertar la nómina
            insert_query = """
                INSERT INTO payroll (employee_id, payroll_period_id, overtime_day_hours, overtime_night_hours, overtime_sunday_hours, overtime_holiday_hours)
                VALUES (:employee_id, :payroll_period_id, :overtime_day_hours, :overtime_night_hours, :overtime_sunday_hours, :overtime_holiday_hours)
            """
            db.session.execute(
                text(insert_query),
                {
                    'employee_id': employee_id,
                    'payroll_period_id': payroll_period_id,
                    'overtime_day_hours': Day_EH,
                    'overtime_night_hours': Nigth_EH,
                    'overtime_sunday_hours': Dom_EH,
                    'overtime_holiday_hours': Fest_EH
                }
            )
            db.session.commit()

            return jsonify({'message': 'Nómina creada correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'error': str(e)}), 500






    @app.route('/api/payroll_detail', methods=['POST'])
    def add_payroll_detail():
        try:
            data = request.get_json()
            concept_id = data.get('concept_id')

            # Obtener el último payroll_id
            last_payroll_id_query = "SELECT MAX(payroll_id) AS last_id FROM payroll"
            result = db.session.execute(text(last_payroll_id_query)).mappings().first()
            last_payroll_id = result['last_id']

            if not last_payroll_id:
                return jsonify({'error': 'No se encontró una nómina existente'}), 400

            # Verificar si el concepto ya fue agregado
            exists_query = """
                SELECT 1 FROM payroll_detail 
                WHERE payroll_id = :payroll_id AND concept_id = :concept_id
            """
            exists = db.session.execute(
                text(exists_query),
                {'payroll_id': last_payroll_id, 'concept_id': concept_id}
            ).first()

            if exists:
                return jsonify({'error2': 'Este concepto ya ha sido agregado a la nómina.'}), 400

            # Si es Auxilio de Transporte (ID 3), verificar salario base
            if concept_id == 3:
                salario_query = """
                    SELECT e.base_salary
                    FROM payroll p
                    JOIN employee e ON p.employee_id = e.employee_id
                    WHERE p.payroll_id = :payroll_id
                """
                salario_result = db.session.execute(text(salario_query), {'payroll_id': last_payroll_id}).mappings().first()
                salario_base = float(salario_result['base_salary'])

                if salario_base > 2847000:
                    return jsonify({'error': 'El empleado no es elegible para Auxilio de Transporte debido a su salario base.'}), 400

            # Insertar el concepto
            insert_query = """
                INSERT INTO payroll_detail (payroll_id, concept_id)
                VALUES (:payroll_id, :concept_id)
            """
            db.session.execute(text(insert_query), {
                'payroll_id': last_payroll_id,
                'concept_id': concept_id
            })
            db.session.commit()

            return jsonify({'message': 'Concepto agregado a la nómina exitosamente'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        
    @app.route('/api/payroll_detail/latest', methods=['GET'])
    def get_latest_payroll_details():
        try:
            # Obtener el último payroll_id
            last_payroll_query = "SELECT MAX(payroll_id) AS last_id FROM payroll"
            last_result = db.session.execute(text(last_payroll_query)).mappings().first()
            last_payroll_id = last_result['last_id']

            if not last_payroll_id:
                return jsonify([])

            # Obtener los conceptos de esa nómina
            detail_query = """
                SELECT 
                    pd.detail_id,
                    pd.concept_id,
                    pc.name,
                    pc.concept_type,
                    pd.value
                FROM payroll_detail pd
                JOIN payroll_concept pc ON pd.concept_id = pc.concept_id
                WHERE pd.payroll_id = :payroll_id
            """

            result = db.session.execute(text(detail_query), {'payroll_id': last_payroll_id}).mappings().all()

            conceptos = [{
                'detail_id': row['detail_id'],
                'concept_id': row['concept_id'],
                'name': row['name'],
                'concept_type': row['concept_type'],
                'value': float(row['value']) if row['value'] else 0.0
            } for row in result]

            return jsonify(conceptos)

        except Exception as e:
            print("ERROR EN /api/payroll_detail/latest:", str(e))
            return jsonify({'error': str(e)}), 500

    @app.route('/api/payroll/latest_summary', methods=['GET'])
    def get_latest_payroll_summary():
        try:
            # Obtener el último payroll_id
            last_payroll_query = "SELECT MAX(payroll_id) AS last_id FROM payroll"
            last_result = db.session.execute(text(last_payroll_query)).mappings().first()
            last_payroll_id = last_result['last_id']

            if not last_payroll_id:
                return jsonify({}), 404

            # Obtener el resumen de la nómina
            summary_query = """
                SELECT 
                    total_earnings,
                    total_deductions,
                    total_to_pay
                FROM payroll
                WHERE payroll_id = :payroll_id
            """

            summary = db.session.execute(text(summary_query), {'payroll_id': last_payroll_id}).mappings().first()

            return jsonify({
                'total_earnings': float(summary['total_earnings']) if summary['total_earnings'] else 0.0,
                'total_deductions': float(summary['total_deductions']) if summary['total_deductions'] else 0.0,
                'total_to_pay': float(summary['total_to_pay']) if summary['total_to_pay'] else 0.0
            })

        except Exception as e:
            print("ERROR EN /api/payroll/latest_summary:", str(e))
            return jsonify({'error': str(e)}), 500



    






    


