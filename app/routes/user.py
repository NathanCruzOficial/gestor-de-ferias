from app.models.tables import User , Vacations
from app.controllers import crud

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from app.models.forms import RegisterForm, VacationForm
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
def home():
    my_vacations = Vacations.query.filter_by(user_id=current_user.id).order_by(Vacations.id.desc()).all()
    form = VacationForm()
    if form.validate_on_submit():
        if current_user.dias_disp > 0:
            data_inicio = form.data_inicio.data
            data_fim = form.data_fim.data
            user_id = current_user.id
            destino = form.destino.data
            motivo = form.motivo.data

            registro_ferias = Vacations(user_id, data_inicio, data_fim, destino, motivo, status=0)
            crud.create(registro_ferias)
            return redirect(url_for("user.home"))
        else:
            flash(f'Seus dias de dispensa acabaram! você tem: {current_user.dias_disp} dias disponíveis', 'danger')

    return render_template("user/home.html", form=form, ferias=my_vacations)

@user_bp.route('/historico')
@required_level(2)
def historico():
    vacations = Vacations.query.join(User).all()
    return render_template("user/historico.html", registros = vacations)

@user_bp.route('/imprimir')
@required_level(2)
def imprimir():
    return render_template("user/imprimir.html")

@user_bp.route('/register', methods=['GET', 'POST'])
@required_level(3)
def register():
    form = RegisterForm()
    users = User.query.all()
    if form.validate_on_submit():
      # Aqui o registro seria processado.
        username = str(form.username.data)
        username = username.upper()

        password = form.password.data
        confirm_password = form.confirm_password.data

        military_id = form.military_id.data

        nome_completo = str(form.nome_completo.data)
        nome_completo = nome_completo.upper()

        posto_grad = form.posto_grad.data
        data_nascimento = form.data_nascimento.data
        nivel = form.nivel.data
        email = str(form.email.data)
        email = email.lower()
        telefone = form.telefone.data

        if confirm_password == password:
            if username in nome_completo:
                if not User.query.filter_by(nome_completo=nome_completo).first():
                    user = User(username=username, password=password, military_id=military_id, nome_completo=nome_completo,dias_disp=0, posto_grad=posto_grad, data_nascimento=data_nascimento, nivel=nivel, email=email, telefone=telefone)

                    crud.create(user)
                    flash('Registro realizado com sucesso!', 'success')
                    return redirect(url_for('user.register'))
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

    return render_template('user/registrador.html', form=form,  users=users)

@user_bp.route('/edit/<int:user_id>', methods=['GET','POST'])
def edit(user_id):
    users = User.query.all()  # Pegue todos os usuários
    return render_template('user/registrador.html', users=users)

@user_bp.route('/delete_user/<int:user_id>', methods=['GET','POST'])
@required_level(3)
def delete_user(user_id):
    # Impede que o usuário logado se exclua
    if current_user.id == user_id:
        return redirect(url_for('user.register'))  # Redireciona para a lista de usuários

    # Encontre o usuário pelo ID e exclua
    crud.delete_user(user_id)
    return redirect(url_for('user.register'))  # Redireciona de volta para a lista de usuários



@user_bp.route('/config')
@required_level(3)
def config():
    return render_template("user/config.html")

@user_bp.route('/logout')
def logout():
    logout_user()  # Encerra a sessão do usuário
    return redirect(url_for('auth.login'))