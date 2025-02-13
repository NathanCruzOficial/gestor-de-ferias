from sqlalchemy.exc import SQLAlchemyError

class DbManager():
    def __init__(self) -> None:
        
        from app import db
        from app.models.tables import User, Vacation

        self.db = db

        self.usuario = User
        self.ferias = Vacation

    def create_user(self,user):
        self.db.session.add(user)
        self.db.session.commit()
        pass

    def reset_db(self):
        try:
            # Remove todos os usuários da tabela
            self.usuario.query.delete()
            self.db.session.commit()



            print("Banco de dados resetado com sucesso!")
        except SQLAlchemyError as e:
            self.db.session.rollback()  # Reverte alterações em caso de erro
            print(f"Erro ao resetar o banco de dados: {str(e)}")

    