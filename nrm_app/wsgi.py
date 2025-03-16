from app import create_app, db
from app.models.admin import AdminModel
from flask_migrate import Migrate
from dotenv import load_dotenv
import os, sys

sys.path.append(os.getcwd())

load_dotenv()

application = create_app(config_name='default')
migrate = Migrate(application, db)


@application.shell_context_processor
def make_shell_context():
    return dict(db=db, Admin=AdminModel)

@application.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


