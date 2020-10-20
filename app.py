import sys
url = sys.path.insert(1, './src/')
from index import app

#Ejecución de la app
if __name__ == '__main__':
    '''
    debug = True para el entorno de desarrollo
    debug = False para el entorno de produccion
    '''
    app.run(debug = False)