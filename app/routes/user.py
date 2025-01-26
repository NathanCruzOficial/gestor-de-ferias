from app.models.tables import Patente, User , Vacation
from app.controllers import crud, db_mannager

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
                return redirect(url_for('user.home'))  # Redireciona para uma página segura
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
    my_vacations = Vacation.query.filter_by(fg_users_id=current_user.id).order_by(Vacation.id.desc()).all()
    form = VacationForm()
    if form.validate_on_submit():
        if current_user.dias_disp == 0:
            fg_users_id = current_user.id
            data_inicio = form.data_inicio.data
            data_fim = form.data_fim.data
            destino = form.destino.data
            motivo = form.motivo.data
            fg_states_id = 1

            registro_ferias = Vacation( fg_users_id, fg_states_id, data_inicio, data_fim, destino, motivo)
            
            crud.create(registro_ferias)
            return redirect(url_for("user.home"))
        else:
            flash(f'Seus dias de dispensa acabaram! você tem: {current_user.dias_disp} dias disponíveis', 'danger')

    return render_template("user/home.html", form=form, ferias=my_vacations)

@user_bp.route('/ferias')
@required_level(2)
def ferias():
    vacations = Vacation.query.join(User).all()
    return render_template("user/ferias.html", registros = vacations)

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
        if form.confirm_password.data == form.password.data:
            if str(form.nome_guerra.data).upper() in str(form.nome_completo.data).upper().split(" "):
                if not db_mannager.user_not_exists(form):
                    message,type = db_mannager.create_user(form)
                    flash(message, type)
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

    user = User.query.get(user_id)  # Pegue o usuário do registro
    # user_dict = user.to_dict()
    form = RegisterForm(obj=user)
    form.submit = False

    if form.validate_on_submit:
        if not db_mannager.user_not_exists(form):
            message,type = db_mannager.update_user(form)
            flash(message, type)
            # return redirect(url_for('user.edit', user_id=user.id))

    if current_user.id == user.id:
        return render_template('user/editor_user.html', user=user, form=form)
    elif current_user.id != user.id and current_user.nivel == 3:
        return render_template('user/editor_user.html', user=user, form=form)
    else:
        return redirect(url_for("user.home"))
    
    

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