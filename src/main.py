from waitress import serve
from router import application

if __name__ == '__main__':
    print("🚀 Сервер запущен на http://127.0.0.1:8080")
    serve(application, host='127.0.0.1', port=8080)