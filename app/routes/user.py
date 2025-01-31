import datetime
from sqlite3 import IntegrityError
from app import db
from app.models.tables import Organizacao, Patente, Secao, User , Vacation , State
from app.controllers import crud, db_mannager

from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request
from flask_login import logout_user, login_required, current_user
from app.models.forms import RegisterForm, UpdateForm, VacationForm,ProfileForm,PasswordChangeForm
from app.controllers import doc_create
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
        dias = (form.data_fim.data - form.data_inicio.data).days
        if current_user.dias_disp >= dias:
            if current_user.dias_disp > 0:
                fg_users_id = current_user.id
                data_inicio = form.data_inicio.data
                data_fim = form.data_fim.data
                destino = form.destino.data
                motivo = form.motivo.data
                fg_states_id = 1

                current_user.dias_disp = current_user.dias_disp - dias

                registro_ferias = Vacation( fg_users_id, fg_states_id, data_inicio, data_fim, destino, motivo)
                print(registro_ferias)
                
                try:
                    crud.create(registro_ferias)
                    db.session.merge(current_user)
                    db.session.commit()                    
                except IntegrityError:
                    db.session.rollback()
                    flash('Erro de Integridade, tente novamente.', 'danger')


                flash('Registro de férias efetuado com sucesso', 'success')
                return redirect(url_for("user.home"))
            else:
                flash(f'Seus dias de dispensa acabaram! você tem: {current_user.dias_disp} dias disponíveis', 'danger')
        else:
            flash(f'Atenção! você tem somente: {current_user.dias_disp} dias disponíveis', 'warning')

    return render_template("user/home.html", form=form, ferias=my_vacations)

@user_bp.route('/ferias')
@required_level(2)
def ferias():
    vacations = Vacation.query.join(User).order_by(Vacation.id.desc()).all()
    return render_template("user/ferias.html", registros = vacations)

# ------------------------------------------------------- IMPRIMIR ---------------------------------------------------------------------
@user_bp.route('/imprimir/archive')
@required_level(2)
def gerar_relatorio():
    # Pegar filtros da URL
    status = request.args.get("status")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    search = request.args.get("search")

    # Construir a query com filtros
    query = Vacation.query

    if status:
        query = query.join(State).filter(State.id == status)
    else:
        status = 0

    if data_inicio:
        query = query.filter(Vacation.data_inicio >= data_inicio)

    if data_fim:
        query = query.filter(Vacation.data_fim <= data_fim)

        

    # Buscar os dados filtrados
    vacations = query.join(User).order_by(Vacation.id.desc()).all()

    status_ferias = {
    0: "TODOS",
    1: "EM ANÁLISE",
    2: "APROVADO",
    3: "REPROVADO",
    4: "EXPIRADO",
    5: "EM ANDAMENTO",
    6: "FINALIZADO"
    }

    status = int(status)
    # Garantir que o status_id seja do tipo inteiro
    status_descricao = status_ferias.get(status, "TODOS")

    niveis = {
    1: "Usuário (Não Autorizado!)",
    2: "Fiscal",
    3: "Administrador"
    }

    nivel = niveis.get(current_user.nivel, "Status desconhecido")


      # Filtros
    filtros = {
        "STATUS": status_descricao,
        "DATA_INI": data_inicio,
        "DATA_FIM": data_fim,
    }

    # Dados fixos
    emissor = {
        "NOME": current_user.nome_completo,
        "DATA": str(datetime.datetime.today().strftime("%d/%m/%Y")),
        "ORGANIZACAO": current_user.organizacao.name,
        "NOME_COMPLETO": current_user.nome_completo,
        "NOME_GUERRA": current_user.nome_guerra,
        "PATENTE": current_user.patente.posto,
        "AUTORIDADE": nivel
    }

    dados = filtros | emissor

    # Criar lista de dados para preencher a tabela do Word
    tabela_dados = [{"state": str(v.state.desc),
                     "om": str(v.user.organizacao.name),
                     "nome": str(v.user.nome_guerra),
                     "p/g": str(v.user.patente.abrev),
                     "data_inicio": v.data_inicio.strftime("%d/%m/%Y"),
                     "data_retorno": v.data_retorno.strftime("%d/%m/%Y"),
                     "contato": f"{v.user.telefone} {v.user.email}",
                     "dias": v.dias} for v in vacations]

    # Criar documento Word filtrado
    output_path = doc_create.preencher_docx(dados, tabela_dados)

    # Retornar o arquivo gerado como download
    return send_file(output_path, as_attachment=True, download_name="relatorio.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@user_bp.route('/imprimir')
@required_level(2)
def imprimir():
    # Pegar os filtros do request
    status = request.args.get("status")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    search = request.args.get("search")

    # Construir a query com filtros dinâmicos
    query = Vacation.query

    if status:
        query = query.join(State).filter(State.id == status)
    if data_inicio:
        query = query.filter(Vacation.data_inicio >= data_inicio)

    if data_fim:
        query = query.filter(Vacation.data_fim <= data_fim)


    # Buscar os resultados filtrados
    vacations = query.join(User).order_by(Vacation.id.desc()).all()

    return render_template("user/imprimir.html", vacations=vacations)


# ----------------------------------------------------------------------------------------------------------------------------


@user_bp.route('/register', methods=['GET', 'POST'])
@required_level(3)
def register():
    form = RegisterForm()
    users = User.query.all()
    if form.validate_on_submit():
        if form.confirm_password.data == form.password.data:
            if str(form.nome_guerra.data).upper() in str(form.nome_completo.data).upper().split(" "):
                if not db_mannager.check_user_exists(form):
                    if not db_mannager.check_unique(form):
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
@required_level(3)
def edit(user_id):

    user_atual = User.query.filter_by(id=user_id).first()  # Pegue o usuário do registro
    form = UpdateForm(obj = user_atual)

    if form.validate_on_submit():
        db_mannager.update_user(user_atual,form)
        return redirect(url_for("user.edit", user_id=user_id))

    return render_template('user/editor_user.html', user_atual=user_atual, form=form)

@user_bp.route('/profile', methods=['GET','POST'])
def profile():
    if not current_user.nivel == 3:
        form = ProfileForm(obj = current_user) # Pegue o registro do usuário logado

        if form.validate_on_submit():
            unique_fields = {
                "email": str(form.email.data).lower(),
                "telefone":form.telefone.data
            }

            for field, value in unique_fields.items():
                if value:  # Verifica se o campo não está vazio ou nulo
                    # Constrói a consulta ao banco
                    query = User.query.filter(getattr(User, field) == value)
                    
                    # Se for edição, exclui o usuário atual da verificação
                    if current_user.id:
                        query = query.filter(User.id != current_user.id)
                    
                    # Verifica se já existe um conflito
                    conflict = query.first()

                    if conflict:
                        flash(f"Erro, o {field} {value} já pertence a outro usuário.", "danger")
                        return redirect(url_for("user.profile"))  # Retorna indicando conflito


            print("Todos os campos estão disponíveis.")
            current_user.email = form.email.data
            current_user.telefone = form.telefone.data

            try:
                db.session.merge(current_user)  # Atualiza os dados do usuário
                db.session.commit()  # Salva as alterações no banco
                flash("Alterações realizadas com sucesso!", "success")
            except Exception as e:
                db.session.rollback()  # Garante que nenhuma alteração parcial seja mantida
                flash(f"Erro inesperado: {str(e)}", "danger")


            return redirect(url_for("user.profile"))  # Retorna indicando conflito
        

        return render_template('user/perfil.html', user_atual=current_user, form=form)
    
    else:
        return redirect(url_for("user.edit", user_id=current_user.id))


@user_bp.route('/delete_user/<int:user_id>', methods=['GET','POST'])
@required_level(3)
def delete_user(user_id):
    # Impede que o usuário logado se exclua
    if current_user.id == user_id:
        return redirect(url_for('user.register'))  # Redireciona para a lista de usuários

    # Encontre o usuário pelo ID e exclua
    crud.delete_user(user_id)
    return redirect(url_for('user.register'))  # Redireciona de volta para a lista de usuários

@user_bp.route('ferias/reprove/<int:registro_id>', methods=['GET','POST'])
@required_level(3)
def reprove_regs(registro_id):
    registro = Vacation.query.get(registro_id)
    if registro and registro.fg_states_id == 1:
        registro.fg_states_id = 3
        registro.user.dias_disp = registro.user.dias_disp + registro.dias

        db.session.merge(registro)
        db.session.commit()
        return redirect(url_for('user.ferias'))

    else:
        flash("Registro não existe", "danger")
        return redirect(url_for('user.ferias'))
    
@user_bp.route('ferias/aprove/<int:registro_id>', methods=['GET','POST'])
@required_level(3)
def aprove_regs(registro_id):
    registro = Vacation.query.get(registro_id)
    if registro and registro.fg_states_id == 1:
        registro.fg_states_id = 2
        db.session.merge(registro)
        db.session.commit()
        return redirect(url_for('user.ferias'))

    else:
        flash(f"Registro não existe", "danger")
        return redirect(url_for('user.ferias'))

@user_bp.route('/config')
@required_level(3)
def config():
    return render_template("user/config.html")

@user_bp.route('/logout')
def logout():
    logout_user()  # Encerra a sessão do usuário
    return redirect(url_for('auth.login'))