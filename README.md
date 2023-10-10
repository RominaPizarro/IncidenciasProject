# IncidenciasProject
[INSTRUCCIONES]

1. Crear el usuario con el script crear_usuario.sql
2. Cargar las tablas de la base de datos db_control_incidencias.sql
3. Ejecutar el proyecto django: python .\manage.py runserver

[USUARIOS]
Usuario administrador
- correo = admin@gmail.com
- username = admin
- password = 123456

Usuario cliente
- correo = anna@gmail.com
- username = anna
- password = 123456

# REST API
- Listar todos los requerimientos. Tipo: GET, URL: api/requerimientos
- Agregar nuevo requerimientos. Tipo: POST, URL: api/requerimientos

Nota: en la carpeta "api" se encuentra el archivo con las peticiones postman para realizar las pruebas.
