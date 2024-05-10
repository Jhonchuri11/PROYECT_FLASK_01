# Importamos flask
from flask import Flask, render_template, request, flash, redirect, url_for
#  importamos para conexion a base de datos
import mysql.connector

# Como breve ayuda utilizamos flash que permite mostrar un mensaje al momento de la ejecuacion de nuestras
# consultas


# crear una aplicacion para comprobar si estamos en el archivo principal

# nombre de la aplicacion
app = Flask(__name__)

# Configuracion usando Pymysql para conectar db 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_PORT'] = 3306

# Inicializar la conexión MySQL
mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    port=app.config['MYSQL_PORT']
)

# Definiendo la sesion para la muestra de mensajes con flash
app.secret_key = 'mysecretkey'

# Inidicar la ruta raiz y crear una vista expresada en una funcion, utilizando decordadores => (extension)
@app.route('/', methods=['GET', 'POST'])
def index():
    #return "<h1>Mi primer Hola Mundo en Flask2</h1>"
    # lista de cursos
    cursos = ['php', 'Python', 'Java', 'Kotlin', 'Delphi']

    data = {
        'titulo': 'index',
        'bienvenido': 'clase 11 Flask',
        'cursos': cursos
    }
    if request.method == "POST":
        details = request.form
        firstName = details['nombre']
        lastName = details['apellido']
        # Lamando la conexion y colocando en variable cursor
        cursor = mysql_conn.cursor()
        cursor.execute("INSERT INTO usuario (nombres, apellidos) VALUES (%s, %s)", (firstName, lastName))
        mysql_conn.commit()
        cursor.close()
        return 'success'
    return render_template("index.html", data=data)

# Ruta para el registro de cliente
@app.route('/add')
def add_client():
    #return "Hola"
    cursor = mysql_conn.cursor()
    cursor.execute('SELECT * FROM cliente')
    # Ejecutamos la consulta
    data = cursor.fetchall()
    return render_template('cliente/index.html', clients = data)

# Ruta para el envio de data y recepcion
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        detalle = request.form
        nombre = detalle['nombre']
        apellido = detalle['apellido']
        edad = detalle['edad']
        cursor = mysql_conn.cursor()
        cursor.execute("INSERT INTO cliente (nombre, apellido, edad) VALUES (%s, %s, %s)", (nombre, apellido, edad))
        mysql_conn.commit()
        # Estamos enviando un mensaje al user despues de la insercion de data
        flash('Cliente agregado correctamente!')
        cursor.close()
        # Al usar redirect + url_for en este caso tenemos que pasarle la funcion
        # para que nos pueda redireccionar a este
        return redirect(url_for('add_client'))
    
#Llamando a un solo dato
@app.route('/edit/<id>')
def get_client(id):
    cursor = mysql_conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE id = %s", (id))
    data = cursor.fetchall()
    print(data)
    return 'recibido'

# Para guardar el edit
#@app.route('/edit/<string:id>')
#def edit_client(id):
#    return id

@app.route('/delete/<string:id>')
def delete_client(id):
    cursor = mysql_conn.cursor()
    cursor.execute('DELETE FROM cliente where id = {0}'.format(id))
    mysql_conn.commit()
    flash('Cliente eliminado correctamente')
    cursor.close()
    return redirect(url_for('add_client'))

if __name__=='__main__':
    app.run(debug=True, port=5000)



