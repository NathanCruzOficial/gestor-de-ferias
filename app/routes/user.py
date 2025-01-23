from app.models.tables import Patente, User , Vacation
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
        print(form)
      # Aqui o registro seria processado.
        nome_guerra = str(form.nome_guerra.data)
        nome_guerra = nome_guerra.upper()

        fg_secao_id = form.secao.data

        password = form.password.data
        confirm_password = form.confirm_password.data

        military_id = form.military_id.data

        fg_organization_id = form.organization.data

        nome_completo = str(form.nome_completo.data)
        nome_completo = nome_completo.upper()

        fg_patente_id = form.patente.data

        data_nascimento = form.data_nascimento.data
        nivel = form.nivel.data
        email = str(form.email.data)
        email = email.lower()
        telefone = form.telefone.data

        dias_disp = current_user.dias_disp

        p = Patente.query.get(fg_patente_id)
        username = p.abrev+nome_guerra

        if confirm_password == password:
            if nome_guerra in nome_completo:
                if not User.query.filter_by(nome_completo=nome_completo,fg_organization_id=fg_organization_id).first():
                    user = User( username, password, military_id, nome_completo, nome_guerra, data_nascimento, nivel,dias_disp, email, telefone, fg_patente_id, fg_organization_id, fg_secao_id)
        

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

    user = User.query.filter_by(id=user_id).first()  # Pegue o usuário do registro
    # user_dict = user.to_dict()
    form = RegisterForm(obj=user)

    if form.validate_on_submit:
        novas_informacoes = User.from_form(form=form, user=user)
        print(novas_informacoes)

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