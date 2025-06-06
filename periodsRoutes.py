
from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db
from datetime import datetime
from audit import audit_log

def periods_data(app):

    @app.route('/periodos')
    def periodos():
        return render_template('partials/payroll_period.html')

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
                ORDER BY pp.payroll_period_id
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
        

    @app.route('/api/payroll_periods', methods=['POST'])
    def create_payroll_period():
        try:
            data = request.get_json()
            type_id = data.get('type_id')
            date_str = data.get('date')  

            if not type_id or not date_str:
                return jsonify({'error': 'Faltan datos requeridos'}), 400

            if int(type_id) not in [1, 2, 3, 4, 5, 6]:
                return jsonify({'error': 'Tipo de nómina inválido'}), 400

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido, debe ser YYYY-MM-DD'}), 400

            if date_obj.day not in [1, 15]:
                return jsonify({'error': 'El día debe ser 1 o 15 del mes'}), 400

            query = text(
                "INSERT INTO payroll_period (payroll_type_id, payroll_date) VALUES (:type_id, :date)"
            )
            db.session.execute(query, {'type_id': type_id, 'date': date_str})
            db.session.commit()
            audit_log(
                action="insert",
                table="payroll_period",
                data_after={
                    "payroll_date": date_str
                },
            )
            return jsonify({'message': 'Periodo creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el periodo:", str(e))
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/payroll-periods-1', methods=['GET'])
    def get_payroll_periods_1():
        try:
            query = """
                SELECT payroll_period_id, payroll_date
                FROM payroll_period
                WHERE payroll_type_id IN (1, 2)
            """
            result = db.session.execute(text(query)).mappings().all()
            periods = []

            for row in result:
                periods.append({
                    'payroll_period_id': row['payroll_period_id'],
                    'payroll_date': row['payroll_date'].strftime('%Y-%m-%d') if row['payroll_date'] else 'Sin fecha'
                })

            return jsonify(periods), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/payroll-periods-2', methods=['GET'])
    def get_payroll_periods_2():
        try:
            query = """
                SELECT payroll_period_id, payroll_date
                FROM payroll_period
                WHERE payroll_type_id IN (3)
            """
            result = db.session.execute(text(query)).mappings().all()
            periods = []

            for row in result:
                periods.append({
                    'payroll_period_id': row['payroll_period_id'],
                    'payroll_date': row['payroll_date'].strftime('%Y-%m-%d') if row['payroll_date'] else 'Sin fecha'
                })

            return jsonify(periods), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/payroll-periods-3', methods=['GET'])
    def get_payroll_periods_3():
        try:
            query = """
                SELECT payroll_period_id, payroll_date
                FROM payroll_period
                WHERE payroll_type_id IN (5)
            """
            result = db.session.execute(text(query)).mappings().all()
            periods = []

            for row in result:
                periods.append({
                    'payroll_period_id': row['payroll_period_id'],
                    'payroll_date': row['payroll_date'].strftime('%Y-%m-%d') if row['payroll_date'] else 'Sin fecha'
                })

            return jsonify(periods), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/payroll-periods-4', methods=['GET'])
    def get_payroll_periods_4():
        try:
            query = """
                SELECT payroll_period_id, payroll_date
                FROM payroll_period
                WHERE payroll_type_id IN (6)
            """
            result = db.session.execute(text(query)).mappings().all()
            periods = []

            for row in result:
                periods.append({
                    'payroll_period_id': row['payroll_period_id'],
                    'payroll_date': row['payroll_date'].strftime('%Y-%m-%d') if row['payroll_date'] else 'Sin fecha'
                })

            return jsonify(periods), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/payroll-periods-5', methods=['GET'])
    def get_payroll_periods_5():
        try:
            query = """
                SELECT payroll_period_id, payroll_date
                FROM payroll_period
                WHERE payroll_type_id IN (4)
            """
            result = db.session.execute(text(query)).mappings().all()
            periods = []

            for row in result:
                periods.append({
                    'payroll_period_id': row['payroll_period_id'],
                    'payroll_date': row['payroll_date'].strftime('%Y-%m-%d') if row['payroll_date'] else 'Sin fecha'
                })

            return jsonify(periods), 200

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)}), 500


