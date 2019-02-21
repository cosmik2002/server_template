from flask import render_template,current_app
from srv.main import bp
from srv import db
from flask_login import login_required,current_user
from datetime import datetime

@bp.route('/')
@bp.route('/index')
@login_required	
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@bp.before_app_request
def before_request():
 if current_user.is_authenticated:
     current_user.last_seen = datetime.utcnow()
     db.session.commit()
