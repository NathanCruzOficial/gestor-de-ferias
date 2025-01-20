from app.models.tables import Users
from app.controllers import crud

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from app.models.forms import RegisterForm
from functools import wraps

# Isntânciando o Blueprint
user_bp = Blueprint('user', __name__)

# Decorador - Limitador de nivel
def required_level(level_required):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if int(current_user.nivel) < level_required:
                return redirect(url_for('user.user'))  # Redireciona para uma página segura
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Middleware para proteger todas as rotas
@user_bp.before_request
@login_required
def require_login():
    """Middleware para exigir login em todas as rotas da Blueprint."""
    pass


# Página principal
@user_bp.route('/', methods=['GET', 'POST'])
def user():
    return render_template("user/home.html")

@user_bp.route('/historico')
def historico():
    return render_template("user/historico.html")

@user_bp.route('/imprimir')
@required_level(2)
def imprimir():
    return render_template("user/imprimir.html")

@user_bp.route('/register', methods=['GET', 'POST'])
@required_level(3)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
      # Aqui o registro seria processado.
        username = form.username.data
        password = form.password.data
        nome_completo = form.nome_completo.data
        posto_grad = form.posto_grad.data
        data_nascimento = form.data_nascimento.data
        nivel = form.nivel.data
        email = form.email.data
        telefone = form.telefone.data

        user = Users(username=username, password=password, nome_completo=nome_completo,dias_disp=0, posto_grad=posto_grad, data_nascimento=data_nascimento, nivel=nivel, email=email, telefone=telefone)

        crud.create(user)
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('user.register'))

    else:
        # Coleta os erros do formulário
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)

    return render_template('user/registrador.html', form=form)

@user_bp.route('/painel')
@required_level(3)
def painel():
    users = Users.query.all()  # Pegue todos os usuários
    return render_template("user/painel.html", users=users)

@user_bp.route('/painel/delete_user/<int:user_id>', methods=['GET','POST'])
@login_required
@required_level(3)
def delete_user(user_id):
    # Impede que o usuário logado se exclua
    if current_user.id == user_id:
        return redirect(url_for('user.painel'))  # Redireciona para a lista de usuários

    # Encontre o usuário pelo ID e exclua
    crud.delete(user_id)
    return redirect(url_for('user.painel'))  # Redireciona de volta para a lista de usuários

@user_bp.route('/config')
@required_level(3)
def config():
    return render_template("user/config.html")

@user_bp.route('/logout')
def logout():
    logout_user()  # Encerra a sessão do usuário
    return redirect(url_for('auth.login'))