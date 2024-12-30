from app import db

class Users(db.Model):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False, default="1234")
    posto_grad = db.Column(db.String(30), nullable=False)
    nome_completo = db.Column(db.String(30), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nivel = db.Column(db.Integer, nullable=False, default=0)
    dias_disp = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)

    def __init__(self, id, username, password, posto_grad, nome_completo, data_nascimento, nivel, dias_disp, email, telefone):
        self.id = id
        self.username = username
        self.password = password
        self.posto_grad = posto_grad
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.nivel = nivel
        self.dias_disp = dias_disp
        self.email = email
        self.telefone = telefone
    
    def __repr__(self):
        return f"<User {self.id}>"

class Vacations(db.Model):
    __tablename__ = "Ferias"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)  # Correção de ForeignKey
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship("Users", foreing_keys=user_id)

    def __init__(self, id, user_id, data_inicio, data_fim, destino, status=0):
        self.id = id
        self.user_id = user_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.destino = destino
        self.status = status

    def __repr__(self):
        return f"<Vacation {self.id} for User {self.user_id}>"
