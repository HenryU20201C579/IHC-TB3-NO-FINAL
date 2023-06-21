from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = '3.82.36.72'
app.config['MYSQL_DATABASE_USER'] = 'support'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sistema.db'
app.config['MYSQL_DATABASE_DB'] = 'tb3'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/singin')
def singin():
    return render_template('singin.html')

@app.route('/singup')
def singup():
    return render_template('singup.html')

@app.route('/services')
def services():
    conexion = mysql.connect()
    print(conexion)
    return render_template('services.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/find_fis')
def find_fis():
    return render_template('find_fis.html')

@app.route('/resultados', methods=["post"])
def resultados():
    nombre = request.form['name']
    distrito = request.form['distrito']
    dia = request.form['dia']
    opcion_horario = request.form['horario']

    # Crear una lista para almacenar las cláusulas de búsqueda
    condiciones = []
    parametros = []

    # Construir la consulta SQL y los parámetros
    consulta = "SELECT * FROM voluntarios"

    if nombre:
        condiciones.append("nombre = %s")
        parametros.append(nombre)

    if distrito:
        condiciones.append("distrito = %s")
        parametros.append(distrito)

    if dia:
        condiciones.append("dias = %s")
        parametros.append(dia)

    if opcion_horario == "Mañana (7:00 - 12:00)":
        condiciones.append("hora_inicio BETWEEN '07:00:00' AND '12:00:00'")
    elif opcion_horario == "Tarde (12:00 - 18:00)":
        condiciones.append("hora_inicio BETWEEN '12:00:00' AND '18:00:00'")
    elif opcion_horario == "Noche (18:00 - 9:00)":
        condiciones.append("hora_inicio BETWEEN '18:00:00' AND '21:00:00'")

    # Combinar las cláusulas de búsqueda si hay alguna
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    print(consulta, parametros)
    
    consulta += ";"


    conexion = mysql.connect()
    cur = conexion.cursor()
    cur.execute(consulta, parametros)
    resultados = cur.fetchall()
    return render_template('resultados.html', resultados = resultados)

@app.route('/find_vol')
def find_vol():
    return render_template('find_vol.html')

@app.route('/ejercicios')
def ejercicios():
    conexion = mysql.connect()
    cur = conexion.cursor()
    cur.execute("select * from ejercicios")
    ejercicios = cur.fetchall()

    return render_template('ejercicios.html', ejercicios = ejercicios)

@app.route('/registro_fis')
def registro_fis():
    return render_template('registro_fis.html')

@app.route('/registro_vol')
def registro_vol():
    return render_template('registro_vol.html')

@app.route('/saveDataEjercicios', methods=['POST'])
def saveDataEjercicios():
    ejercicio = request.form['ejercicio']
    repeticiones = request.form['repeticiones']
    fecha = request.form['fecha']

    data = (ejercicio, repeticiones, fecha)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("insert into ejercicios (ejercicio, repeticiones, fecha) values ( %s, %s, %s);", data)
    conexion.commit()


    return redirect('/ejercicios')

@app.route('/saveDataVoluntario', methods=['POST'])
def saveDataVoluntario():
    #lunes, martes, miercoles, jueves, viernes, sabado, domingo = "hola"
    # if request.method == 'POST':
    #     print(request.form.getlist('jueves'))
    
    nombre = request.form['name']
    distrito = request.form['distrito']

    dias = []
    dias.append(request.form.getlist('lunes'))
    dias.append(request.form.getlist('martes'))
    dias.append(request.form.getlist('miercoles'))
    dias.append(request.form.getlist('jueves'))
    dias.append(request.form.getlist('viernes'))
    dias.append(request.form.getlist('sabado'))
    dias.append(request.form.getlist('domingo'))
    
    hora_inicio = request.form['hora_inicio']
    hora_final = request.form['hora_final']

    actividades = []
    actividades.append(request.form.getlist('Pasear al aire libre'))
    actividades.append(request.form.getlist('Hacer ejercicio'))
    actividades.append(request.form.getlist('Cocinar'))
    actividades.append(request.form.getlist('Artesanía o manualidades'))
    actividades.append(request.form.getlist('Jardinería'))
    actividades.append(request.form.getlist('Lectura'))

    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    for var in dias: 
        if (var != [] and hora_inicio != "" and hora_final != "" and (hora_inicio < hora_final) and nombre != "" and distrito != ""):
            for var2 in actividades: 
                if (var2 != []):
                    data = (var, nombre, hora_inicio, hora_final, distrito, var2)
                    cursor.execute("insert into voluntarios (dias, nombre, hora_inicio, hora_final, distrito, actividades) values (%s, %s, %s, %s, %s, %s);", data)
                    conexion.commit()

    return redirect('/registro_vol')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")