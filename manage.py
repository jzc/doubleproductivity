#!/usr/bin/env python
#TODO: remove flask_script, flask has a cli interface
import inspect

from flask_script import Manager, Shell

from app import create_app, db
import app.models as classes

app = create_app("development")
manager = Manager(app)
models = {name: class_ for name, class_ in inspect.getmembers(classes, inspect.isclass)}

def make_shell_context():
    return dict(app=app, db=db, **models)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def create_test_data():
    """Makes random test data."""
    from tests.create_test_data import create_test_data
    create_test_data(db, models)

@manager.command
def test():
    """Runs all tests."""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()