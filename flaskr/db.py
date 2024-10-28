import sqlite3
import click
from flask import current_app, g # 'g' is a special obj that i unique for each request.
    # Used to store data that might be accessed by multiple functions during request. 


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close
    
def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f: # open_resource opens a file relative to the flaskr package,
        #which is useful since you won’t necessarily know where that location is when deploying the application later. 
        # get_db returns a database connection, which is used to execute the commands read from the file.
        db.executescript(f.read().decode('utf8'))
        
@click.command('init-db') # Defines CLI called init-db that calls the function show shows the message to the user
def init_db_command():
    init_db()
    click.echo('initialised the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db) # Tells Flask to call that function when cleaning up after returning the response.
    app.cli.add_command(init_db_command) # Adds a new command that can be called with the flask command.