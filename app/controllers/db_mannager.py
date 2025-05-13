from datetime import datetime
from app import app,db
from app.models.tables import User, Vacation, Patente, State
from app.controllers import crud
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from flask import flash
import pandas as pd
from werkzeug.security import generate_password_hash

def db_update(user):
    db.session.merge(user)
    db.session.commit()

def create_user(form):
    
    with app.app_context():  # Garante que você está no contexto da aplicação
        patente = Patente.query.get(form.fg_patente_id.data)
        patente = str(patente.abrev)

        dados = [
        {
            "username":f"{patente} {form.nome_guerra.data}",
            "password": form.password.data.strip() if form.password.data else "null",  # Você pode armazenar uma hash da senha usando bcrypt ou similar
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

            return f'Registro realizado com sucesso! Usuário: {novo_usuario.username}', 'success'

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

        if user_exists and user_exists == usuario and not data_exists:            
            # Atualiza os dados do usuário
            usuario.username =  str(f"{patente} {form.nome_guerra.data}").upper()
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

            if nome_guerra_presente(usuario.nome_guerra, usuario.nome_completo):
                try:
                    db.session.merge(usuario)  # Atualiza os dados do usuário
                    db.session.commit()  # Salva as alterações no banco
                    flash("Alterações realizadas com sucesso!", "success")
                except IntegrityError as e:
                    db.session.rollback()  # Reverte as alterações no banco em caso de erro
                    flash("Erro de integridade: dados duplicados ou conflitantes!", "danger")
                except Exception as e:
                    db.session.rollback()  # Garante que nenhuma alteração parcial seja mantida
                    flash(f"Erro inesperado: {str(e)}", "danger")
            else:
                flash("O nome de guerra deve pertencer ao nome completo.", "warning")
        

        elif user_exists and user_exists != usuario:
             flash(f"O usuário da {user_exists.organizacao.name} chamado {user_exists.patente.abrev} {user_exists.nome_guerra} já existe.", "danger")


        elif not user_exists and not data_exists:
             # Atualiza os dados do usuário
            usuario.username =  str(f"{patente} {form.nome_guerra.data}").upper()
            usuario.nome_guerra = str(form.nome_guerra.data).upper()
            usuario.fg_organization_id = form.fg_organization_id.data
            usuario.fg_patente_id = form.fg_patente_id.data

            if nome_guerra_presente(usuario.nome_guerra, usuario.nome_completo):
                try:
                    db.session.merge(usuario)  # Atualiza os dados do usuário
                    db.session.commit()  # Salva as alterações no banco
                    flash("Alterações realizadas com sucesso!", "success")
                except IntegrityError as e:
                    db.session.rollback()  # Reverte as alterações no banco em caso de erro
                    flash("Erro de integridade: dados duplicados ou conflitantes!", "danger")
                except Exception as e:
                    db.session.rollback()  # Garante que nenhuma alteração parcial seja mantida
                    flash(f"Erro inesperado: {str(e)}", "danger")
            else:
                flash("O nome de guerra deve pertencer ao nome completo.", "warning")

def nome_guerra_presente(nome_guerra, nome_completo):
    # Converter para maiúsculas e dividir em palavras
    nome_guerra = set(nome_guerra.upper().split())
    nome_completo = set(nome_completo.upper().split())

    # Retorna True se todos os nomes de nome_guerra estiverem dentro de nome_completo
    return nome_guerra.issubset(nome_completo)


# ================================================= REGISTROS ===============================================================================

def periodo_disponivel(fg_users_id, data_inicio, data_fim):
        from sqlalchemy import or_, and_
        from datetime import timedelta

        data_retorno = data_fim + timedelta(days=1)

        # Verifica se já existem férias registradas nesse intervalo
        conflito = Vacation.query.join(State).filter(
            Vacation.fg_users_id == fg_users_id,
            or_(
                # Se data_inicio estiver dentro de outro período de férias
                Vacation.data_inicio.between(data_inicio, data_retorno),
                # Se data_fim estiver dentro de outro período de férias
                Vacation.data_retorno.between(data_inicio, data_retorno),
                # Se um período já registrado engloba completamente o novo período
                and_(Vacation.data_inicio <= data_inicio, Vacation.data_retorno >= data_retorno)
            )
        ).first()

        restrict = ['analise','aprovada','consumindo','finalizado']

        print(data_inicio,"    ",data_fim)

        if conflito:
            if conflito.state.abrev in restrict:
                return False
            else:
                return True
        else:
            return True



def atualizar_registros():
    registros = Vacation.query.all()
    
    # hoje_str = "2025-02-17"
    # hoje = datetime.strptime(hoje_str, "%Y-%m-%d").date()

    hoje = datetime.today().date()  # Converte para datetime.date
    print(hoje)


    if not registros:
        return  # Retorna sem fazer nada se não houver registros

    for registro in registros:

        # print("Verificando registro", type(today), " com as datas",type(registro.data_fim)," ", type(registro.data_inicio) )

        if hoje >= registro.data_fim:
            if registro.fg_states_id == 5:  # Em Andamento → Finalizado
                registro.fg_states_id = 6
                db.session.merge(registro)

            elif registro.fg_states_id == 4:  # Expirado → Excluir
                db.session.delete(registro)

        elif hoje >= registro.data_inicio:
            if registro.fg_states_id == 2:  # Aprovado → Em andamento
                registro.fg_states_id = 5
                db.session.merge(registro)

            elif registro.fg_states_id == 1:  # Em Análise → Expirado
                registro.fg_states_id = 4
                db.session.merge(registro)

            elif registro.fg_states_id == 3:  # Reprovado → Em andamento
                db.session.delete(registro)

    
    db.session.commit()  # Realiza um único commit ao final para eficiência

def reset_database():
    from app.models.seed import seed_data

    try:
        db.drop_all()
        db.create_all()
        seed_data()

        print('reset concluído')

    except Exception as e:
        print(f'{e} : erro ao resetar banco de dados')



def processar_linha(row, index):
    try:
        military_id = str(row.get("military_id")).strip()
        if not military_id:
            raise ValueError("military_id obrigatório")

        user_data = {
            "username": str(row.get("username") or f"user{index}").upper(),
            "password": generate_password_hash("1234"),  # sempre resetando a senha padrão
            "military_id": military_id,
            "nome_completo": str(row.get("nome_completo") or "NOME DESCONHECIDO").upper(),
            "nome_guerra": str(row.get("nome_guerra") or "GUERRA").upper(),
            "data_nascimento": pd.to_datetime(row.get("data_nascimento"), errors='coerce'),
            "nivel": int(row.get("nivel") or 1),
            "dias_disp": int(row.get("dias_disp") or 0),
            "email": str(row.get("email") or f"user{index}@exemplo.com").lower(),
            "telefone": str(row.get("telefone") or "00000000000"),
            "fg_patente_id": int(row.get("fg_patente_id") or 1),
            "fg_organization_id": int(row.get("fg_organization_id") or 1),
            "fg_secao_id": int(row.get("fg_secao_id") or 1),
        }

        if pd.isna(user_data["data_nascimento"]):
            raise ValueError("Data de nascimento inválida")

        return user_data
    except Exception as e:
        print(f"[Erro na linha {index+2}] {e}")
        return None


def importar_usuarios_substituir_tudo(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)

    db.session.query(User).delete()
    db.session.commit()

    for index, row in df.iterrows():
        user_data = processar_linha(row, index)
        if not user_data:
            continue
        try:
            user = User(**user_data)
            db.session.add(user)
        except exc.SQLAlchemyError as e:
            print(f"[Erro ao inserir linha {index+2}] {e}")

    db.session.commit()
    print("Importação concluída com substituição total.")


def importar_usuarios_atualizar(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)

    for index, row in df.iterrows():
        user_data = processar_linha(row, index)
        if not user_data:
            continue

        user = User.query.filter_by(military_id=user_data["military_id"]).first()

        try:
            if user:
                # Atualiza campos existentes
                for key, value in user_data.items():
                    if key != "password":  # não atualiza senha automaticamente aqui
                        setattr(user, key, value)
                print(f"Usuário atualizado: {user_data['military_id']}")
            else:
                # Cria novo usuário
                novo_user = User(**user_data)
                db.session.add(novo_user)
                print(f"Usuário criado: {user_data['military_id']}")
        except exc.SQLAlchemyError as e:
            print(f"[Erro ao processar linha {index+2}] {e}")

    db.session.commit()
    print("Importação concluída com atualização de dados.")

def gerar_modelo_excel_usuarios(caminho_arquivo="modelo_usuarios.xlsx", incluir_exemplo=False):
    # Inspeciona as colunas do modelo User
    mapper = inspect(User)
    colunas = [col.name for col in mapper.columns if col.name != "id"]

    # Linha de exemplo (opcional)
    dados_exemplo = {
        "military_id": "123456",
        "username": "EXEMPLO",
        "password": "1234",
        "nome_completo": "FULANO DA SILVA",
        "nome_guerra": "FULANO",
        "data_nascimento": "1990-01-01",
        "nivel": 1,
        "dias_disp": 10,
        "email": "fulano@example.com",
        "telefone": "21999999999",
        "fg_patente_id": 1,
        "fg_organization_id": 1,
        "fg_secao_id": 1,
    }

    if incluir_exemplo:
        df = pd.DataFrame([dados_exemplo])[colunas]
    else:
        df = pd.DataFrame(columns=colunas)

    df.to_excel(caminho_arquivo, index=False)
    print(f"Modelo salvo em: {caminho_arquivo}")

    