from flask import Blueprint, render_template, request, jsonify, send_file
import hashlib
import base64
import io
from cryptography.fernet import Fernet

views = Blueprint('views', __name__)



@views.route('/')
@views.route('/main_page')
def main_page():
    return render_template('main_page.html')


@views.route('/home')
def home():
    return render_template('home.html')



def generate_hash(data, hash_type):
    try:
        hash_function = getattr(hashlib, hash_type)()
        hash_function.update(data.encode('utf-8'))
        return hash_function.hexdigest()
    except AttributeError:
        return None
    
    
    
@views.route('/gen_hash', methods=['POST'])
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


@views.route('/hash_check')
def hash_check():    
    return render_template('hash_check.html')


def generate_file_key(passcode):
    key = hashlib.sha256(passcode.encode()).digest()
    return base64.urlsafe_b64encode(key[:32])



#####   Allow user to pick hash algorithm type if I have time   #####
@views.route('/file_encrypt', methods=['GET', 'POST'])
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
        
        print(request.files)
        print(request.form)
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