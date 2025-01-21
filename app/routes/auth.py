from app.controllers.crud import create_admin
from app.models.tables import User
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from app.models.forms import LoginForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    create_admin()
    form = LoginForm()
    if form.validate_on_submit():        
        username = str(form.username.data)
        username = username.upper()

        user = User.query.filter_by(username=username, posto_grad=form.posto_grad.data).first()
        if user and user.check_password(form.password.data):  # Usando o método check_password
            login_user(user)
            return redirect(url_for('user.home'))
        else:
            flash("Usuário ou senha inválidos.","warning")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)
