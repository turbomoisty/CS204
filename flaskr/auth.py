import functools
import re

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None
        
        if not re.match("^[A-Za-z0-9]+$", username):
            error = 'Username is required'
            
        if password:
            if len(password) < 8:
                error = 'Password length must be at least 8'

        elif not password:
            error = 'Password is required'
            
            
        elif not email:
            error = 'Email is required'
            
        elif not re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            error = "Please enter a valid email"
            
        if error is None:
            try:
                db.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", 
                           (username, generate_password_hash(password), email),)
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
        
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() # returns one row from query.
            # If the query doesn't return a result, it returns None
        if user is None:
            error = 'Incorrect Username'
        elif not check_password_hash(user['password'], password): # check_password_hash hashes submitted pw in the same manner as the
            # stored hash, and if they match, the PW is valid.
            error = 'Incorrect Password'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            print("User ID Set in Session:", session['user_id'])  # Debug: Confirm user_id is set in session

            return redirect(url_for('views.main_page'))
        
        flash(error)
    return render_template('auth/login.html')
        
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    
    @functools.wraps(view) #???
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view