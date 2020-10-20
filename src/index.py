import os
from datetime import timedelta
from flask import (Flask, 
    render_template, 
    send_from_directory, 
    request, 
    redirect, 
    flash, 
    url_for,
    g,
    session)
from flask_mysqldb import MySQL
from login import users

#Configuraciones de la base de datos
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'd1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'uzjkks7j0ro99jby'
app.config['MYSQL_PASSWORD'] = 'wyzmp61glnwaxewy'
app.config['MYSQL_DB'] = 'ma4j48xxoy3udlvp'
mysql = MySQL(app)

#Definimos clave y duración de la sesión
secret_key = os.urandom(12).hex()
app.config['SECRET_KEY'] = secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config.update(SESSION_COOKIE_SECURE = True)


#Ruta principal
@app.route('/')
def home():
    """
    Obtenemos la informacion de los productos destacados
    :return: devuelve el template home.html con la información de los productos destacados
    """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products ORDER BY product_id DESC LIMIT 6')
    data = cur.fetchall()
    return render_template('home.html', products = data)

#Ruta para agregar suscriptores
@app.route('/add_suscriber', methods=['POST'])
def add_suscriber():
    if request.method == 'POST':
        #Ejecutamos la consulta para subir la direccion de correo
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (user_email) VALUES('{0}')".format(email))
        mysql.connection.commit()
        #Devolvemos mensaje flash
        flash('Muchas gracias por suscribirte')
        return redirect(url_for('home'))

#Ruta para eliminar suscriptores
@app.route('/delete_suscriber', methods=['POST'])
def delete_suscriber():
    if request.method == 'POST':
        #Ejecutamos la consulta para eliminar la direccion que coincida con la del input del usuario
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_email = '{0}'".format(email))
        mysql.connection.commit()
        flash('Tu desuscripción se llevo a cabo con éxito. Esperamos que vuelvas pronto')
        return redirect(url_for('home'))

#Ruta de la pagina Acerca De
@app.route('/about')
def about():
    """
    :return: retorna template about.html
    """
    return render_template('about.html')

#Ruta de la página de Productos
@app.route('/products')
def products():
    """
    Obtenemos lista de productos que esten en stock
    :return: retornamos el template products.html con la información acerca de los productos y las categorias
    """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products WHERE stock = 1 ORDER BY category ASC')
    products_data = cur.fetchall()
    cur.execute('SELECT category FROM products GROUP BY category ORDER BY category')
    categories_list = cur.fetchall()
    return render_template('products.html', products = products_data, categories = categories_list)

#Ruta de la página de un Producto en especifico
@app.route('/products/<int:id>')
def product_view(id):
    """
    Vista de un producto
    :param id: int
    :return: retorna el template product_view.html con informacion del producto
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE product_id = '{}'".format(id))
    product_data = cur.fetchall()[0]
    return render_template('product_view.html', product = product_data)

#Ruta del icono de la pagina
@app.route('/icon.ico')
def favicon():
    """
    :return: ruta del icono
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
    'icon.ico', mimetype= 'image/vnd.microsoft.icon')

@app.before_request
def before_request():
    """
    El usuario global se define a None. Si hay un usuario en la sesión lo agregamos a la variable global.
    Si se hace una peticion que no esta dentro del subdominio /admin, y no es una ruta excepcional definida en 
    additional_URL, eliminamos el usuario de la sesión. Si este no es el caso, la sesión se elimina a los 5 minutos
    :return: None
    """
    g.user = None
    additional_URL = ['/static/<path:filename>', 'None']
    if 'username' in session:
        #Obtenemos los objetos instanciados con el mismo username
        user = [index for index in users if index.username == session['username']][0]
        g.user = user
    if '/admin' not in str(request.url_rule) and str(request.url_rule) not in additional_URL:
        #Si la ruta no pertenece a /admin y no esta en la lista additional_URL, entonces eliminamos la sesión
        session.pop('username', None)

@app.route('/login', methods=['POST','GET'])
def login():
    """
    Sistema de inicio de sesión. Si el usuario y la contraseña ingresados coinciden con el de algun usuario instanciado en login.py,
    se redirecciona a /admin y se agrega el usuario a la sesión. Sino, devolvemos un mensaje flash avisando del error.
    :return: retorna template login.html y en el caso de hacer un ingreso de sesión válido redirecciona a /admin.
    """
    if request.method == 'POST':
        #Obtenemos datos del formulario
        username = request.form['username']
        password = request.form['password']
        try:
            user = [index for index in users if index.username == username][0]
        except IndexError:
            #Si no hay usuario con un username igual devolvemos un mensaje
            flash('El usuario ingresado no existe.')
            return redirect(url_for('login'))
        if user and user.password == password:
            #Eliminamos cualquier sesión ya iniciada
            session.clear()
            #Agregamos el usuario a la sesión
            session['username'] = user.username
            #Mantenemos la sesión para que no se mantenga tras cerrar el navegador
            session.permanent = False
            return redirect(url_for('admin'))
        else:
            flash('La contraseña no coincide con la del usuario')
            return redirect(url_for('login'))
    return render_template('login.html')

#Ruta de la pagina del administrador
@app.route('/admin')
def admin():
    """
    Si no hay un usuario global definido, redirecciona al inicio de sesión. Dentro de /admin se muestra 
    información sobre los productos y usuarios. Se pueden eliminar productos, acceder a la edición y agregado de productos;
    y contactar con usuarios.
    :return: retorna template admin.html con información de los productos y usuarios
    """
    if not g.user:
        return redirect(url_for('login'))
    #Añadimos a la sesión el atributo logged para administrar la necesidad de volver a iniciar sesión o no
    session['logged'] = True
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    return render_template('admin.html', products = products, users = users)

@app.route('/admin/add_product', methods=['POST', 'GET'])
def add_product():
    """
    Pagina para agregar productos. Si no hay usuario, redirecciona a /login.
    :return: retorna template edit_page.html
    """
    if request.method == 'POST':
        category = request.form['Categoria']
        description = request.form['Descripcion']
        URL = request.form['URL']
        stock = request.form.get('Stock')
        if stock == 'Stock':
            stock = 1
        else:
            stock = 0
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO products (category, description, img_dir, stock) VALUES('{category}','{description}','{URL}',{stock})")
        mysql.connection.commit()
        flash('El producto se ha agregado con éxito')
        return redirect(url_for('admin'))
    if 'username' in session and 'logged' in session:
        return render_template('edit_page.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/edit_product/<int:id>', methods=['POST', 'GET'])
def edit_product(id):
    """
    Pagina para editar productos. Si no hay usuario, redirecciona a /login. Hace una petición a la base de datos
    para obtener información actualizada del producto a actualizar.
    :param id: int
    :return: retorna template edit_page.html
    """
    if request.method == 'POST':
        category = request.form['Categoria']
        description = request.form['Descripcion']
        URL = request.form['URL']
        stock = request.form.get('Stock')
        if stock == 'Stock':
            stock = 1
        else:
            stock = 0
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE products SET category = '{category}', description = '{description}', img_dir = '{URL}', stock = {stock} WHERE product_id = {id}")
        mysql.connection.commit()
        flash('El producto se ha editado con éxito')
        return redirect(url_for('admin'))
    if 'username' in session and 'logged' in session:
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT * FROM products WHERE product_id = {id}')
        product_data = cur.fetchall()[0]
        return render_template('edit_page.html', product = product_data)
    else:
        return redirect(url_for('login'))

@app.route('/admin/delete_product', methods=['POST'])
def delete_product():
    """
    Si el ID del producto es válido y la palabra CONFIRMAR se ingresa correctamente, se elimina el producto
    con el ID correspondiente
    :return: redirreciona a /admin
    """
    if request.method == 'POST' and request.form['confirm'] == 'CONFIRMAR':
        product_id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE product_id = '{0}'".format(product_id))
        mysql.connection.commit()
        flash('El producto se ha eliminado con éxito del inventario')
        return redirect(url_for('admin'))
    elif request.method == 'POST' and request.form['confirm'] != 'CONFIRMAR':
        flash('Intente de nuevo')
        return redirect(url_for('admin'))

@app.errorhandler(404)
def not_found(error):
    """
    :return: retorna template para errores código 404
    """
    return render_template('not_found.html'), 404