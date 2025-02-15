from datetime import datetime, timedelta
from app import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Função de carregamento do usuário
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ===================================================USUARIOS============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Aumentando o tamanho para suporte a hash
    military_id = db.Column(db.String(30), unique=True, nullable=False)
    nome_completo = db.Column(db.String(30), unique=True, nullable=False)
    nome_guerra = db.Column(db.String(30), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nivel = db.Column(db.Integer, nullable=False, default=0)
    dias_disp = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    telefone = db.Column(db.String(30), unique=True, nullable=False)

    fg_secao_id = db.Column(db.Integer, db.ForeignKey('secoes.id'), nullable=False)
    fg_organization_id = db.Column(db.Integer, db.ForeignKey('organizacoes.id'), nullable=False)
    fg_patente_id = db.Column(db.Integer, db.ForeignKey('patentes.id'), nullable=False)


    patente = db.relationship("Patente",  back_populates='users')
    organizacao = db.relationship("Organizacao",  back_populates='users')
    secao = db.relationship("Secao",  back_populates='users')
                                
    ferias = db.relationship("Vacation",  back_populates='user')


    def __init__(self, password="1234", military_id=None, nome_completo=None, nome_guerra=None, data_nascimento=None, nivel=None, email=None, telefone=None, fg_patente_id=None, fg_organization_id=None, fg_secao_id=None,username=None, dias_disp=0):
        
        # self.patente = Patente.query.get(fg_patente_id)
        # self.organizacao = Organizacao.query.get(fg_organization_id)
        # self.secao = Secao.query.get(fg_secao_id)

        self.fg_secao_id = fg_secao_id
        self.fg_organization_id = fg_organization_id
        self.fg_patente_id = fg_patente_id
    
        self.username = str(username).upper()
        self.nome_guerra = str(nome_guerra).upper()
        self.password = generate_password_hash(password)  # Armazenando a senha de forma segura
        self.military_id = military_id
        self.nome_completo = str(nome_completo).upper()
        self.data_nascimento = data_nascimento
        self.nivel = nivel
        self.dias_disp = dias_disp
        self.email = str(email).lower()
        self.telefone = telefone
        

    def get_id(self):
        return str(self.id)  # Retorne o ID como string, necessário para o Flask-Login
    
    def __repr__(self):
        return f"<User {self.username},id: {self.id}>"

    def check_password(self, password="0"):
        return check_password_hash(self.password, password)  # Método para verificar a senha
    
    def set_password(self, password):
        self.password = generate_password_hash(password)



# ===================================================FERIAS============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class Vacation(db.Model):
    __tablename__ = "vacations"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    data_retorno = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(30), nullable=False)
    motivo = db.Column(db.String(255))
    dias = db.Column(db.Integer, nullable=False)

    fg_users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fg_states_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    

    user = db.relationship("User", back_populates='ferias')
    state = db.relationship("State", back_populates='ferias')


    def __init__(self, fg_users_id, data_inicio, data_fim, dias, destino, motivo,fg_states_id=1):

        self.user = User.query.get(fg_users_id)
        self.state = State.query.get(fg_states_id)

   
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.data_registro = datetime.today()
        self.destino = destino

        self.motivo = motivo

        # Verificando se as datas são válidas antes de calcular os dias
        if self.data_inicio and self.data_fim:
            self.dias = dias
        else:
            self.dias = 0  # Ou outro valor padrão se as datas forem None

        print("DIA DA SEMANA:   ",data_fim.weekday())

        if data_fim.weekday() == 4:
            self.data_retorno = data_fim + timedelta(days=3)   
        elif data_fim.weekday() == 5:
            self.data_retorno = data_fim + timedelta(days=2)
        else:
            self.data_retorno = data_fim + timedelta(days=1)

    def __repr__(self):
        return f"<Vacation {self.id} for User {self.user.username}>"

# ===================================================OMS============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class Organizacao(db.Model):
    __tablename__ = 'organizacoes'
    id = db.Column(db.Integer, primary_key=True)
    abrev = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    users = db.relationship("User",  back_populates='organizacao')

    def __init__(self,abrev,name):
        self.abrev = abrev
        self.name = name


# ===================================================SEÇÕES============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class Secao(db.Model):
    __tablename__ = 'secoes'
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    users = db.relationship("User",  back_populates='secao')

    def __init__(self,section,email):
        self.section = section
        self.email = email


# ===================================================POSTO============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class Patente(db.Model):
    __tablename__ = 'patentes'
    id = db.Column(db.Integer, primary_key=True)
    abrev = db.Column(db.String(50), nullable=False)
    posto = db.Column(db.String(50), nullable=False)

    users = db.relationship("User",  back_populates='patente')

    def __init__(self,abrev,posto):
        self.abrev = abrev
        self.posto = posto

# ===================================================STATUS============================================================================================
# -------------------------------------------------------------------------------------------------------------------------------------------------------
class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    abrev = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(50), nullable=False)

    ferias = db.relationship("Vacation", back_populates='state')

    def __init__(self,abrev,desc):
        self.abrev = abrev
        self.desc = desc
