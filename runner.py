from gevent.pywsgi import WSGIServer
from server import app


if __name__ == '__main__':
    host = ''
    port = 5050
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()

