from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/contactanos')
def contactanos():
    return render_template('sitio/contactanos.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")