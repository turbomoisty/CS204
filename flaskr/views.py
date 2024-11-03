from flask import Blueprint, render_template


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/main_page')
def main_page():
    return render_template('home.html')

@views.route('hash_check')
def hash_check():
    return render_template('hash_check.html')

@views.route('file_encrypt')
def file_encrypt():
    return render_template('file_encrypt.html')