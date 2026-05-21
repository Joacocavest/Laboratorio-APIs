from waitress import serve
from servicios_domicilio.wsgi import application

if __name__ == '__main__':
    print("Iniciando el servidor Waitress en http://localhost:8000...")
    serve(application, host='127.0.0.1', port=8000)