from app.models.tables import Users

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from app.models.forms import LoginForm   

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username= form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('user.user'))
        else:
            flash("Usuário Inválido")
            return redirect(url_for('auth.login'))


    return render_template('auth/login.html', form=form)