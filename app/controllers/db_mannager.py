from app import app,db
from app.models.tables import User, Vacation, Patente, Secao
from app.controllers import crud
from sqlalchemy.exc import IntegrityError

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

def check_unique(form):
    data_exists = User.query.filter(
        (User.nome_completo == form.nome_completo.data) |
        (User.military_id == form.military_id.data) |
        (User.email == form.email.data) |
        (User.telefone == form.telefone.data)
    ).first()
    if not data_exists:
        return True
       
        
def check_user_exists(form):
    user_exists = User.query.filter_by(
            nome_guerra=form.nome_guerra.data,
            fg_patente_id=form.fg_patente_id.data,
            fg_organization_id=form.fg_organization_id.data
        ).first()
    if not user_exists:
        return True

def update_user(dados_antigos, form):
    with app.app_context():  # Garante que você está no contexto da aplicação
        patente = Patente.query.get(form.fg_patente_id.data)
        patente = str(patente.abrev)

        dados = [
        {   
            "username":f"{patente}{form.nome_guerra.data}",
            "password": dados_antigos.password,
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
        if not check_user_exists(form):
            print("Usuário Existe")

            if check_unique

            for user_data in dados:
                novos_dados = User(**user_data)

            print(dados_antigos.id)
            print(novos_dados.id)

            if not dados_antigos.id == novos_dados.id:
                print("prosseguir")
                


        else:
            print("voltar")