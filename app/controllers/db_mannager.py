from colorama import reinit
from app import app,db
from app.models.tables import User, Vacation, Patente, Secao
from app.controllers import crud
from sqlalchemy.exc import IntegrityError
from flask import flash

def create_user(form):
    
    with app.app_context():  # Garante que você está no contexto da aplicação
        patente = Patente.query.get(form.fg_patente_id.data)
        patente = str(patente.abrev)

        dados = [
        {
            "username":f"{patente}{form.nome_guerra.data}",
            "password": form.password.data,  # Você pode armazenar uma hash da senha usando bcrypt ou similar
            "military_id": form.military_id.data,
            "fg_patente_id": form.fg_patente_id.data,  # Relacionado ao ID da patente (exemplo: Soldado = 1)
            "nome_completo": form.nome_completo.data,
            "nome_guerra": form.nome_guerra.data,
            "fg_organization_id": form.fg_organization_id.data,  # Relacionado ao ID da organização (exemplo: "Cia C GUEs - 9ª Bda Inf Mtz")
            "fg_secao_id": form.fg_secao_id.data,  # Relacionado ao ID da seção
            "data_nascimento": form.data_nascimento.data,  # Formato string para facilitar conversão posterior
            "nivel": form.nivel.data,  # 3 representa "Administrador"
            "email": form.email.data,
            "telefone": form.telefone.data
        }
        ]

        for user_data in dados:
            novo_usuario = User(**user_data)

        try:
            db.session.add(novo_usuario)  # Adiciona
            db.session.commit()

            return 'Registro realizado com sucesso!', 'success'

        except IntegrityError:
            return 'Dados Inválidos!', 'danger'
    
    # -----------=-=------------------------------------------=-=-------------------------------

def check_unique(form,current_user_id=None):
    unique_fields = {
        "nome_completo": str(form.nome_completo.data).upper(),
        "military_id": form.military_id.data,
        "email": str(form.email.data).lower(),
        "telefone":form.telefone.data
    }

    for field, value in unique_fields.items():
        if value:  # Verifica se o campo não está vazio ou nulo
            # Constrói a consulta ao banco
            query = User.query.filter(getattr(User, field) == value)
            
            # Se for edição, exclui o usuário atual da verificação
            if current_user_id:
                query = query.filter(User.id != current_user_id)
            
            # Verifica se já existe um conflito
            conflict = query.first()

            if conflict:
                flash(f"O campo '{field}' com o valor '{value}' já pertence a outro usuário: {conflict.username}.", "danger")
                return True  # Retorna True indicando conflito


    print("Todos os campos estão disponíveis.")
    return False  # Nenhum conflito encontrado

       
        
def check_user_exists(form):
    user_exists = User.query.filter_by(
            nome_guerra=str(form.nome_guerra.data).upper(),
            fg_patente_id=form.fg_patente_id.data,
            fg_organization_id=form.fg_organization_id.data
        ).first()
    if user_exists:
        return user_exists
    else:
        return None

def update_user(usuario, form):
    with app.app_context():  # Garante que você está no contexto da aplicação
        patente = Patente.query.get(form.fg_patente_id.data)
        patente = str(patente.abrev)

        user_exists = check_user_exists(form)

        data_exists = check_unique(form,usuario.id)

        print("user_atual: ", usuario)
        print("dados_check: ", user_exists)

        if user_exists and user_exists == usuario:            
            if not data_exists:

                # Atualiza os dados do usuário
                usuario.username =  str(f"{patente}{form.nome_guerra.data}").upper()
                usuario.military_id = form.military_id.data
                usuario.nome_completo = str(form.nome_completo.data).upper()
                usuario.nome_guerra = str(form.nome_guerra.data).upper()
                usuario.data_nascimento = form.data_nascimento.data
                usuario.nivel = form.nivel.data
                usuario.dias_disp = form.dias_disp.data
                usuario.email = str(form.email.data).lower()
                usuario.telefone = form.telefone.data
                usuario.fg_secao_id = form.fg_secao_id.data
                usuario.fg_organization_id = form.fg_organization_id.data
                usuario.fg_patente_id = form.fg_patente_id.data

                # db.session.commit()  # Salva as alterações no banco
                flash("Alterações realizadas com sucesso!", "success")
        
        elif not user_exists and not data_exists:
            print("Continuar")
            print("Trocar Usuário e Checar dados pessoais")
            

        else:
            flash("!erro","danger")
            # flash(f"O usuário da {user_exists.organizacao.name} chamado {user_exists.patente.abrev} {user_exists.nome_guerra} já existe.", "danger")