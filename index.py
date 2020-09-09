import os
from flask import Flask, render_template, send_from_directory, request, redirect, flash, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' #sql10.freemysqlhosting.net , mysql-12563-0.cloudclusters.net
app.config['MYSQL_USER'] = 'root' #sql10364048 , Bati
app.config['MYSQL_PASSWORD'] = '' #RYuAGkygdA , Bautista01
app.config['MYSQL_DB'] = 'Caelum' #sql10364048 , Caelum
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products ORDER BY product_id DESC LIMIT 6')
    data = cur.fetchall()
    return render_template('home.html', products = data)

@app.route('/add_suscriber', methods=['POST'])
def add_suscriber():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (user_email) VALUES('{0}')".format(email))
        mysql.connection.commit()
        flash('Muchas gracias por suscribirte')
        return redirect(url_for('home'))

@app.route('/delete_suscriber', methods=['POST'])
def delete_suscriber():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_email = '{0}'".format(email))
        mysql.connection.commit()
        return redirect(url_for('home'))

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
    app.run(debug = True)