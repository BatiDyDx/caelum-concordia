import os
from flask import Flask, render_template, send_from_directory, request, redirect, flash, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'd1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'uzjkks7j0ro99jby'
app.config['MYSQL_PASSWORD'] = 'wyzmp61glnwaxewy'
app.config['MYSQL_DB'] = 'ma4j48xxoy3udlvp'
mysql = MySQL(app)

secret_key = os.urandom(12).hex()
app.config['SECRET_KEY'] = secret_key

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
        flash('Tu desuscripción se llevo a cabo con éxito. Esperamos que vuelvas pronto')
        return redirect(url_for('home'))

@app.route('/delete_page')
def delete_page():
    return render_template('delete.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products ORDER BY category ASC')
    data = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute('SELECT category, COUNT(product_id) FROM products GROUP BY category ORDER BY category')
    data2 = cur.fetchall()
    return render_template('products.html', products = data, categories = data2)

@app.route('/product/<string:id>')
def product_view(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE product_id = '{}'".format(id))
    data = cur.fetchall()
    return render_template('product_view.html', product = data)

@app.route('/icon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
    'icon.ico', mimetype= 'image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug = True)