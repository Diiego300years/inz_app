from gevent import monkey
monkey.patch_all()
import redis
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from config import config
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import JWTManager
from app.services import socketio
from app.services.dashboard_socket import DashboardNamespace

jwt = JWTManager()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
csrf = CSRFProtect()

# I decided to use several configuration sets
def create_app(config_name):
    config_name = os.getenv('FLASK_CONFIG', 'default')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bcrypt.init_app(app)
    moment.init_app(app)

    from .auth.login_manager import login_manager
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    redis_client = redis.StrictRedis(
        host='nrm_redis',
        port=6379,
        db=0,
        decode_responses=True
    )
    app.config['REDIS_CLIENT'] = redis_client

    dn = DashboardNamespace('/')
    # namepsaces for socketio
    socketio.on_namespace(dn)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .edit import edit as edit_blueprint
    app.register_blueprint(edit_blueprint, url_prefix='/edit')

    dn.update_dashboard_data(app, socketio)

    return app
