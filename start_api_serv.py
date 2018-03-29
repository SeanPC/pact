
import os
import sys
import pecan

from wsgiref.simple_server import make_server

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)


conf = pecan.configuration.conf_from_file('/pact/httpservice/config.py')
import app as app_mod
app = app_mod.setup_app(conf)

host, port = conf.server.host, int(conf.server.port)
srv = make_server(host, port, app)

print('Starting server in PID %s' % os.getpid())

if host == '0.0.0.0':
    print(
        'serving on 0.0.0.0:%s, view at http://127.0.0.1:%s' %
        (port, port)
    )
else:
    print("serving on http://%s:%s" % (host, port))

try:
    srv.serve_forever()
except KeyboardInterrupt:
    # allow CTRL+C to shutdown
    pass







