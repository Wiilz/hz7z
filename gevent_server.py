from gevent.pywsgi import WSGIServer
from run import app

http_server = WSGIServer(('127.0.0.1', 5001), app)
http_server.serve_forever()
