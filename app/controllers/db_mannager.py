from app import app,db
from app.models.tables import User, Vacations
from app.controllers import crud

def reset_users():
# Exclui todos os registros da tabela 'User'
    with app.app_context():  # Garante que você está no contexto da aplicação
        db.session.query(User).delete()
        db.session.commit()
        crud.create_admin()
        ...