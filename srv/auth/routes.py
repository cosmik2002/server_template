from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from srv import db
from srv.auth import bp
from srv.auth.forms import LoginForm, RegistrationForm
from srv.models import User

 
@bp.route('/login', methods=['GET', 'POST'])
def login():
    #current_app.logger.info('login %s %s',request.method,request.form)
    if current_user.is_authenticated and login.login_fresh():
      current_app.logger.info(curren_user.name+'logged')
      return redirect(url_for('main.index'))
    current_app.config['SQLALCHEMY_BINDS']['supermag'] = 'firebird://nub:0@serv2:3050/e:\\supermag.gdb?charset=utf8'
    res = db.get_engine(bind='supermag').execute("select name,full_name from users_v")
    form = LoginForm()
    form.username.choices = [(r.name,r.full_name) for r in res]
    res.close()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
          flash('invalid username or password '+form.username.data)
          return redirect(url_for('auth.login'))
        login_user(user,remember=form.remember_me.data)
        current_app.config['SQLALCHEMY_BINDS']['supermag'] = 'firebird://'+form.username.data+':'+form.password.data+'@serv2:3050/e:\\supermag.gdb?charset=utf8'
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)