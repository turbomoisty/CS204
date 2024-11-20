from flask import Blueprint, render_template, request, jsonify, send_file, redirect, url_for,flash
from flaskr.db import get_db
from flask_login import current_user,login_required
import hashlib
from  werkzeug.security import generate_password_hash
import base64
import re
import io
from cryptography.fernet import Fernet

views = Blueprint('views', __name__)

def generate_hash(data, hash_type): #Generated hash 
    try:
        hash_function = getattr(hashlib, hash_type)()
        hash_function.update(data.encode('utf-8'))
        return hash_function.hexdigest()
    except AttributeError:
        return None
    

@views.route('/gen_hash', methods=['POST']) #For the hash check page, when selecting has value
def generate_hash_route():
    data = request.json.get('data')
    hash_type = request.json.get('hash_type')
    hash_value = generate_hash(data, hash_type)
    try:
        if hash_value:
            return jsonify({'hash': hash_value}),200
    except Exception as _:
        
        return jsonify({'error': 'Invalid hash'}),400


@views.route('/check_hash',methods=['POST'])
def compare_hash():
    hash_left =request.json.get('hash_l')
    hash_right = request.json.get('hash_r')
    compare_result = (hash_left == hash_right)
    return jsonify({'match': compare_result}), 200

@views.route('/generate_file_hash', methods=['POST'])
def gen_file_hash():
    file = request.files.get('file')
    if file:
        hash_type= request.form.get('hash_type')


        hash_function = getattr(hashlib, hash_type)()
        for segment in file.stream:
            hash_function.update(segment)
        return jsonify({'hash': hash_function.hexdigest()}),200
    
    no_file = 'No file detected. Pleaase provide one before proceeding.'
    return render_template('file_encrypt.html', error_message=no_file),400


def generate_file_key(passcode): ##just for file encryption
    key = hashlib.sha256(passcode.encode()).digest()
    return base64.urlsafe_b64encode(key[:32])


##----Page routes-----s##



@views.route('/')
@views.route('start_page')
def start_page():
    return render_template('start_page.html')


@views.route('/main_page')
def main_page():
    return render_template('main_page.html')


@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/hash_check')
def hash_check():    
    return render_template('hash_check.html')

        

#####   Allow user to pick hash algorithm type if I have time   #####
@views.route('/file_encrypt', methods=['GET', 'POST'])
@login_required
def file_encrypt():
    if request.method == 'POST':
        passCode = request.form['passcode']
        action = request.form['action']
        file = request.files['file']
        
        if not passCode or not file:
            no_file = 'No file detected or passcode has not been provided.'
            return render_template('file_encrypt.html', error_message=no_file),400
    
        key = generate_file_key(passCode)
        f_key = Fernet(key)
        file_data = file.read()
        
        if action == 'encrypt':
            encrypted_file = f_key.encrypt(file_data)
            file_name = file.filename + '.encrypted'
            return send_file(io.BytesIO(encrypted_file), mimetype='application/octet-stream', as_attachment=True,download_name=file_name)
        
        # Currently there is a bug that will randomly display error box on page load. Unable to replicae it consistenty atm.
        elif action == 'decrypt':
            try:
                decrypted_file = f_key.decrypt(file_data)
                # Current issue --- attemping to replace value to None or '' results in invalid password.
                file_name = file.filename.replace('.encrypted','.remove_me')
                return send_file( io.BytesIO(decrypted_file), mimetype='application/octet-stream', as_attachment=True, download_name=file_name)
            
            except Exception as _:
                error = "Invalid passcode or given format"
                return render_template('file_encrypt.html', error_message=error), 400
    return render_template('file_encrypt.html')


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    db = get_db()
    user_id = current_user.id
    error = None
    # Fetch the current user's details
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not username or not email:
            error = 'Username and email are required.'
        elif new_password and new_password != confirm_password:
            error = 'Passwords do not match.'
        elif new_password and len(new_password) < 8:
            error = '--Password must be at least 8 characters long--'
        elif not re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            error = 'Invalid email format.'
            
        elif new_password == password:
            error = 'your new password cannot be'
        if error is None:
            try:
                if new_password:
                    password = generate_password_hash(new_password)
                db.execute('UPDATE user SET username = ?, email = ?, password = ? WHERE id = ?',
                           (username, email, password, user_id))
                db.commit()
                flash('Account updated successfully.')
                return redirect(url_for('views.main_page'))
            except db.IntegrityError:
                error = 'Username or email already taken.'
        flash(error)
    return render_template('settings.html', user=user)
