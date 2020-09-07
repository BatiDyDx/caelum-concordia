import os
from flask import Flask, render_template, send_from_directory
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'#sql10.freemysqlhosting.net
app.config['MYSQL_USER'] = 'root'#sql10364048
app.config['MYSQL_PASSWORD'] = ''#RYuAGkygdA
app.config['MYSQL_DB'] = 'Caelum'#sql10364048
mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products ORDER BY product_id DESC LIMIT 6')
    data = cur.fetchall()
    return render_template('home.html', products = data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products ORDER BY name ASC')
    data = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute('SELECT name, COUNT(product_id) FROM products GROUP BY name ORDER BY name')
    data2 = cur.fetchall()
    return render_template('productos.html', products = data, categories = data2)

@app.route('/icon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
    'icon.ico', mimetype= 'image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(port = 5000, debug = True)

