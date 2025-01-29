from app.models.tables import Organizacao, User
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from app.models.forms import LoginForm

from app.models.seed import seed_data


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    # seed_data()
    form = LoginForm()
    if form.validate_on_submit():        
        username = str(form.username.data)
        username = username.upper()

        user = User.query.filter_by(username=username, fg_organization_id=form.fg_organization_id.data).first()
        if user:
            if user and user.check_password(form.password.data):  # Usando o método check_password
                login_user(user)
                return redirect(url_for('user.home'))
            else:
                flash("Senha incorreta.","danger")
                return redirect(url_for('auth.login'))
        else:
            flash("Usuário não existe.","danger")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)
