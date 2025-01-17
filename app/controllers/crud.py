from app import db
from app.models.tables import Users
from flask_login import current_user

# Comandos CRUD

def create(user):
    db.session.add(user)
    db.session.commit()

def delete(user):
    if current_user.id != user:  # Impede que o próprio usuário se exclua
        user_to_delete = Users.query.get(user)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()


# Função para atualizar um usuário
def update(user_id, new_data):
    try:
        user = Users.query.get(user_id)  # Busca o usuário pelo ID
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