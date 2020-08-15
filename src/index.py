import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contacto.html')

@app.route('/product')
def product():
    return render_template('productos.html')

@app.route('/icon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
    'icon.ico', mimetype= 'image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug = True)