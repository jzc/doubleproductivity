#!/usr/bin/env python
import inspect

from app import create_app, db
import app.models as classes

app = create_app("development")
models = {name: class_ for name, class_ in inspect.getmembers(classes, inspect.isclass)}

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, **models)

@app.cli.command()
def create_test_data():
    """Makes random test data."""
    from tests.create_test_data import create_test_data
    create_test_data(db, models)

@app.cli.command()
def test():
    """Runs all tests."""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)