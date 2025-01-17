import os
from dotenv import load_dotenv
from app.services import socketio
from wsgi import application

# dontenv_prod_path = ".env.prod"

load_dotenv()

wsgi_app = os.getenv("GUNICORN_APP")


# # Info is not the most important. For future maybe 2 handlers or sth
loglevel = os.getenv('GUNICORN_LOG_LEVEL')


# # Binding port 5000
bind = os.getenv('GUNICORN_BIND')

# # Only localhost for now, in future * for all ips
forwarded_allow_ips = os.getenv('GUNICORN_FORWARDED_ALLOW_IPS')
proxy_allow_ips = os.getenv('GUNICORN_PROXY_ALLOW_IPS')


# For Flask-SocketIO should be only 1 worker
workers = 1
worker_class = os.getenv('GUNICORN_WORKER_CLASS')

# # With this could be fun giving more and more xD
# threads = int(os.environ.get('GUNICORN_THREADS', '4'))
#
# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
#


# # # What should headers have

reload = os.getenv('GUNICORN_RELOAD')

# # Optional ssl, for prod must 2 == require, for now optional
cert_reqs = os.getenv('GUNICORN_CERT_REQS')

# timeout = 120
# keepalive = 25

# Set True if you want to see if config is okay. Return 0 mean it's okay
# check_config = False

# Better visualization
# print_config = True
#
accesslog = os.getenv('GUNICORN_ACCESS_LOG')
access_log_format = os.getenv('GUNICORN_LOG_FORMAT')

# certfile = os.getenv('GUNICORN_SSL_CERTFILE')
# keyfile = os.getenv('GUNICORN_SSL_KEYFILE')

cors_allowed_origins = os.getenv('GUNICORN_CORS_ALLOWED_ORIGINS')

secure_scheme_headers = {
    'X-Forwarded-Proto': os.getenv('GUNICORN_PROXY_FORWARDED_PROTO'),
    'X-Forwarded-SSL': os.getenv('X-FORWARDED-SSL'),
    'X-Forwarded-PROTOCOL': os.getenv('X-FORWARDED-PROTOCOL'),
    'Access-Control-Allow-Origin': os.getenv('ACCESS-CONTROL-ALLOW-ORIGIN'),
    'Access-Control-Allow-Credentials': os.getenv('ACCESS-CONTROL-ALLOW-CREDENTIALS')
}


# def when_ready(server):
#     """Hook Gunicorn: Uruchomienie wątku nasłuchującego Redis."""
#     print("Gunicorn is ready. Starting Redis listener...")
#     start_background_task(application, socketio)