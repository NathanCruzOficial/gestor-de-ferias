from app import db
from app.models.tables import User
from flask_login import current_user
from datetime import datetime

# Comandos CRUD

def create(dataclass):
    db.session.add(dataclass)
    db.session.commit()

def delete_user(user):
    if current_user.id != user:  # Impede que o próprio usuário se exclua
        user_to_delete = User.query.get(user)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()

def create_admin():
    count = User.query.count()
    if count == 0:  # Tabela vazia
        ...


# Função para atualizar um usuário
def update(user_id, new_data):
    try:
        user = User.query.get(user_id)  # Busca o usuário pelo ID
        if user:
            # Atualiza os campos do usuário com os novos dados
            for key, value in new_data.items():
                setattr(user, key, value)
            db.session.commit()  # Confirma a alteração no banco de dados
            print(f"Usuário com ID {user_id} foi atualizado.")
        else:
            print(f"Usuário com ID {user_id} não encontrado.")
    except Exception as e:
        db.session.rollback()  # Em caso de erro, desfaz qualquer mudança
        print(f"Erro ao atualizar o usuário: {e}")