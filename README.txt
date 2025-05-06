README.txt

Proyecto Final – Base de Datos 2
Sistema de Gestión de Nómina

INTEGRANTES DEL GRUPO:
- David Santiago García Preciado – CC 1016948620 – dgarciapr@unbosque.edu.co
- Fernando Javier Alvarado  – CE 519860 – falvaradoa@unbosque.edu.co
- Jorge Orlando Jaramillo – CC 1002559352 – jjaramillon@unbosque.edu.co
Fecha: 24/04/2025

DESCRIPCIÓN DEL CONTENIDO DE LOS SCRIPTS:

1. Script de Creación de Objetos (creacion_objetos.sql)
-------------------------------------------------------
Este script contiene la creación de todas las tablas necesarias para el sistema de gestión de nómina, incluyendo:

- app_user: Tabla para el manejo de usuarios del sistema.
- department: Tabla de dependencias o departamentos.
- employee_position: Tabla de cargos o puestos de trabajo.
- employee: Registro detallado de empleados.
- payroll_concept: Conceptos utilizados en la nómina (devengados y deducciones).
- payroll_type: Tipos de nómina (quincenal, mensual, primas, etc.).
- payroll_period: Períodos de liquidación.
- payroll: Encabezado de cada liquidación de nómina.
- payroll_detail: Detalle de conceptos aplicados a cada liquidación.
- audit: Tabla de auditoría que registra operaciones sobre tablas clave.

Además, este script incluye la definición de **funciones y triggers** para:
- Auditoría automática (triggers AFTER INSERT/UPDATE/DELETE).
- Cálculo de conceptos aplicados a empleados.
- Actualización automática de totales devengados, deducidos y a pagar.

2. Script de Inserción de Registros (insercion_datos.sql)
---------------------------------------------------------
Contiene datos simulados para poblar las tablas creadas, incluyendo:

- Cargos y departamentos.
- Empleados con información personal y laboral.
- Conceptos de nómina (como salario base, auxilio de transporte, EPS, pensión, horas extras).
- Tipos de nómina y períodos correspondientes.
- Liquidaciones de nómina para distintos empleados.
- Detalles de conceptos aplicados a liquidaciones específicas.

Permite verificar el funcionamiento del sistema con datos de prueba.

3. Scripts Varios (funciones_y_triggers.sql)
--------------------------------------------
Incluye funciones y triggers especializados que automatizan tareas del sistema:

- `calculate_overtime_value`: Calcula el valor total por horas extra basándose en el salario y los porcentajes definidos por tipo de hora (diurna, nocturna, dominical, festiva).
- `calculate_concept_employee_value`: Asigna automáticamente el valor monetario correspondiente a un concepto de nómina según el salario del empleado y las condiciones del concepto.
- `update_total_payroll`: Calcula y actualiza los totales devengados, deducidos y netos a pagar por cada liquidación.
- Triggers `AFTER INSERT` para detonar estas funciones automáticamente cuando se registran nuevos conceptos en la liquidación.

INSTRUCCIONES DE USO:
----------------------
1. Ejecutar el script `creacion_objetos.sql` en el motor de base de datos PostgreSQL.
2. Ejecutar el script `insercion_datos.sql` para cargar la información de prueba.
3. Validar el funcionamiento de las funciones y triggers insertando registros adicionales en `payroll_detail`.
4. Verificar la tabla `audit` para evidencias de auditoría automática.

NOTAS FINALES:
--------------
- El sistema está diseñado para asegurar integridad de datos mediante claves foráneas.
- Todas las funciones y triggers están escritos en PL/pgSQL.
- Los scripts pueden ejecutarse de forma modular o completa, según se requiera.

