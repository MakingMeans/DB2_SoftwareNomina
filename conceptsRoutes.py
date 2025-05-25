from flask import render_template, jsonify, request
from sqlalchemy.sql import text
from models import db
from audit import audit_log

def concepts_data(app):
    

    @app.route('/conceptos')
    def conceptos():
        return render_template('partials/conceptos.html')


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
                ORDER BY concept_id
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
        
    @app.route('/api/conceptos', methods=['POST'])
    def create_concept():
        try:
            data = request.get_json()
            nombre = data.get('nombre')
            tipo = data.get('tipo')
            descripcion = data.get('descripcion', '')
            porcentaje = data.get('porcentaje')

            if not nombre or not tipo:
                return jsonify({'error': 'Nombre y tipo son requeridos'}), 400

            if tipo not in ('earning', 'deduction'):
                return jsonify({'error': 'Tipo inválido'}), 400

            query = text("""
                INSERT INTO payroll_concept (name, concept_type, description, percentage, fixed_value)
                VALUES (:nombre, :tipo, :descripcion, :porcentaje, NULL)
            """)
            db.session.execute(query, {
                'nombre': nombre,
                'tipo': tipo,
                'descripcion': descripcion,
                'porcentaje': porcentaje
            })
            db.session.commit()
            audit_log(
                action="insert",
                table="employee",
                data_after={
                    "concept_name": nombre
                },
            )
            return jsonify({'message': 'Concepto creado correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            print("Error al crear el concepto:", str(e))
            return jsonify({'error': str(e)}), 500

    @app.route('/api/conceptos/select_1', methods=['GET'])
    def get_conceptos_select_1():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre
                FROM payroll_concept
                WHERE concept_id IN (1, 2, 3, 4)
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/conceptos/select_2', methods=['GET'])
    def get_conceptos_select_2():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre
                FROM payroll_concept
                WHERE concept_id IN (11, 12, 13, 14, 15, 16)
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/conceptos/select_3', methods=['GET'])
    def get_conceptos_select_3():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre
                FROM payroll_concept
                WHERE concept_id IN (9)
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/conceptos/select_4', methods=['GET'])
    def get_conceptos_select_4():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre
                FROM payroll_concept
                WHERE concept_id IN (10)
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  

    @app.route('/api/conceptos/select_5', methods=['GET'])
    def get_conceptos_select_5():
        try:
            query = """
                SELECT 
                    concept_id AS id,
                    name AS nombre
                FROM payroll_concept
                WHERE concept_id IN (5, 6, 7, 8)
            """
            result = db.session.execute(text(query)).mappings()

            conceptos = [
                {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
                for row in result
            ]

            return jsonify(conceptos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  