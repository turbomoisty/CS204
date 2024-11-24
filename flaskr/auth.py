import functools
from re import match
from flask_login import login_user, logout_user
from .models import User

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db



bp = Blueprint('auth', __name__, url_prefix='/auth')#

@bp.route('/register', methods=['GET','POST']) #associates the /register with the function below.
def register():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None
        
        if not match("^[A-Za-z0-9]+$", username): #Does not allow for special characters
            error = 'valid username is required'
            
        elif password:
            if len(password) < 8:
                error = 'Password length must be at least 8'
        #Check logic poperly for multiple if/elifs
        elif not match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            error = 'Invalid email format.'
            
        if error is None:
            try:
                db.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", 
                           (username, generate_password_hash(password), email),)#takes the query with the ? placeholders with user input
                            # Since it's not safe to store PWs directly, use gph from werkzeug
                db.commit()
                
                user_list = db.execute("SELECT * FROM user").fetchall()
                print("User List:", user_list)
            except db.IntegrityError:
                error = f"User {username} already exists"
                
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')



@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user_row = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if (user_row is None) or (not check_password_hash(user_row['password'], password)): #If entered has doesnt match existing hash, give error
            error = 'Incorrect username or password'
    
        if error is None:
            user = User.from_db_row(user_row)  #Convert database row to User object
            login_user(user) 
            return redirect(url_for('views.main_page'))
        flash(error)
    return render_template('auth/login.html')

        
@bp.route('/logout')
def logout():
    session.clear() #Currently I can't seem to clear user session... TO be fixed
    logout_user()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view) #???
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


