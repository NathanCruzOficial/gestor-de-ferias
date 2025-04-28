from app.models.tables import Organizacao, User
from app.controllers import db_mannager
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from app.models.forms import LoginForm, RegisterForm, Userform
from app.models.seed import seed_data
from .middlewares import redirect_if_authenticated

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@redirect_if_authenticated  # Impede o acesso se o usuário já estiver logado
def user():
    # seed_data()
    form = Userform()
    if form.validate_on_submit():        
        username = str(form.username.data)
        username = username.upper()

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password is None:
                flash("Primeiro Login! Crie sua primeira senha.","warning")
                return redirect(url_for('auth.register', user_id=user.id))
            else:
                return redirect(url_for('auth.login', user_id=user.id))
        else:
            flash("Usuário não existe! favor comunicar a seção de informática da sua Unidade.","danger")
            return redirect(url_for('auth.user'))

    return render_template('auth/entry.html', form=form)

@auth_bp.route('/login/<user_id>', methods=['GET', 'POST'])
@redirect_if_authenticated  # Impede o acesso se o usuário já estiver logado
def login(user_id):
    form = LoginForm()
    if form.validate_on_submit():        
        username = str(form.username.data)
        username = username.upper()

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password is None:
                flash("Primeiro Login! Crie sua primeira senha.","warning")
                return redirect(url_for('auth.login'))
            elif user and user.check_password(form.password.data):  # Usando o método check_password
                db_mannager.update_join_date(user)
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('user.home'))
            else:
                flash("Senha incorreta.","danger")
                return redirect(url_for('auth.login'))
        else:
            flash("Usuário não existe.","danger")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form, user=user_id)

@auth_bp.route('/sing_in/<user_id>', methods=['GET', 'POST'])
@redirect_if_authenticated  # Impede o acesso se o usuário já estiver logado
def register(user_id):
    users = User.query.all()
    user = User.query.filter_by(id=user_id).first()
    form = RegisterForm(obj=user)
    username = user.username
    if form.validate_on_submit():
        if form.confirm_password.data == form.password.data:
            # if str(form.nome_guerra.data).upper().split(" ") in str(form.nome_completo.data).upper().split(" "):
            if db_mannager.nome_guerra_presente(form.nome_guerra.data, form.nome_completo.data):
                if not db_mannager.check_user_exists(form):
                    if not db_mannager.check_unique(form):
                        message,type = db_mannager.create_user(form)
                        flash(message, type)
                    return redirect(url_for('auth.login'))
                else:
                    flash('Usuário Já Existe!', 'danger')
            else:
                flash('O nome de guerra deve pertencer ao nome completo!', 'warning')
        else:
            flash('As senhas não coicidem!', 'warning')

    else:
        # Coleta os erros do formulário
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)

    return render_template('auth/criar_conta.html', form=form, users=users, user=username)
