from flask import Blueprint, render_template,request, jsonify, send_file, redirect
import hashlib
import os
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/main_page')
def main_page():
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
    if hash_value:
        return jsonify({'hash': hash_value}),200
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

    return jsonify({'error': 'File has not been provided'}),400

@views.route('/hash_check')
def hash_check():    
    return render_template('hash_check.html')


@views.route('/file_encrypt', methods=['GET', 'POST'])
def file_encrypt():
    if request.method == 'POST':
        passCode = request.form['passcode']
        action = request.form['action']
        file = request.files['file']
        
        if file:
            filename = sec_file(file.filename)
            file_path = os.path.join(views.config['UPLOAD_FOLDER'],  filename)
            file.save(file_path)
            
            hash_key = generate_hash(file, 'SHA256')
            output_file_p = os.path.join(views.config['ENCRYPTED_FOLDER'], f"{action}_{filename}")
        
        
        
    return render_template('file_encrypt.html')