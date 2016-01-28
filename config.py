import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

##
# Database settings
##
DB_HOST = 'localhost'
DB_NAME = 'scoremodel'
DB_USER = 'scoremodel'
DB_PASS = 'Kpg70PHzdbhOmXIkaTxNOSkCO7JFhlyPQ1jXyJITo2YX1QJH9lfjL9l86X1M0DW'

##
# Flask-WTF
##
WTF_CSRF_ENABLED = True
SECRET_KEY = 'ufdVFllYyTFkotTJZEmrnY8eSwgEoiLYjOmJyCqCxUe0medrGV4J1kTqlIgqq89'

##
# Babel
##
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

##
# Debug settings
##
if DEBUG is True:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passw}@{host}/{db}'.format(user=DB_USER, passw=DB_PASS,
                                                                          host=DB_HOST, db=DB_NAME)
