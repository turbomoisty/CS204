from flask import Blueprint, render_template


views = Blueprint('views', __name__)



@views.route('/')
@views.route('/main_page')
def main_page():
    return render_template('flex.html')