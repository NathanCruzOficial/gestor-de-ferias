from app import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Função de carregamento do usuário
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Aumentando o tamanho para suporte a hash
    military_id = db.Column(db.String(30), unique=True, nullable=False)
    posto_grad = db.Column(db.String(30), nullable=False)
    nome_completo = db.Column(db.String(30), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nivel = db.Column(db.Integer, nullable=False, default=0)
    dias_disp = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
                                
    def __init__(self, username, password, military_id, posto_grad, nome_completo, data_nascimento, nivel, dias_disp, email, telefone):
        self.username = username
        self.password = generate_password_hash(password)  # Armazenando a senha de forma segura
        self.military_id = military_id
        self.posto_grad = posto_grad
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.nivel = nivel
        self.dias_disp = dias_disp
        self.email = email
        self.telefone = telefone

    def get_id(self):
        return str(self.id)  # Retorne o ID como string, necessário para o Flask-Login
    
    def __repr__(self):
        return f"<User {self.id}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Método para verificar a senha




class Vacations(db.Model):
    __tablename__ = "vacations"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(30), nullable=False)
    motivo = db.Column(db.String(255))
    dias = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    

    usuarios = db.relationship("User", foreign_keys=user_id)  # Referência direta ao usuário

    def __init__(self, user_id, data_inicio, data_fim, destino, motivo, status=0):
        self.user_id = user_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.destino = destino
        self.motivo = motivo
        self.status = status

        # Verificando se as datas são válidas antes de calcular os dias
        if self.data_inicio and self.data_fim:
            self.dias = (self.data_fim - self.data_inicio).days
        else:
            self.dias = 0  # Ou outro valor padrão se as datas forem None

    def __repr__(self):
        return f"<Vacation {self.id} for User {self.usuarios.username}>"
