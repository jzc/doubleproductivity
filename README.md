# technicallyimpressive

Milestones are located in the [docs](/docs) folder.

## What is this?

This is the repo for CS Connections, a group project for CSCI 3308 done by Justin Cai, Matt Menten, Ellie Puls, David Doan, and Eli Jacobshagen.
CS Connections is a social media site for CU computer science students to discuss computer science courses, find tutors, upload class notes/resources, and more.

## Running

To run this app, Python 3 and `pipenv`. This can be installed using 

    $ pip install pipenv

Once installed, you can download all dependencies by using 

    $ pipenv install

This will create a virtualenv with all the necessary packages.
After ou create a virtualenv, you should run 

    $ ./add_flask_app.sh

This will add some extra lines to the `bin/activate` file of this project's virtualenv.
More specifically, it will allow you to not have to enter these command everytime your start your 
virtualenv:

    $ export FLASK_APP=technicallyimpressive.py
    $ export FLASK_DEBUG=1

These commands are necessary for flask to find the correct app to run.
To start the test server, start the virtualenv by running 

    $ pipenv shell

and then do

    (venv) $ flask run

This will start a development server.
There are other command available through `flask` as well, such as

* `flask create_test_data`: You'll most likely want to run this to populate the database with some dummy data.
* `flask test`: Run all unittests
* `flask shell`: Start a python interactive shell in an app context with some useful app specific classes imported in already.

## Project structure

* `/`: contains project configuration files
* `/docs`: milestones
* `/tests`: contains files for testing the app
* `/app`: root directory of the app, contains global application functions and app factory
* `/app/static`: static files such as js, css, etc.
* `/app/templates`: contains all html templates for the app
* `/app/auth`: code for login, register, etc.
* `/app/home`: home blueprint for the site; code for homepage
* `/app/course`: logic for course pages