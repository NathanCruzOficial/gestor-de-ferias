from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = 'segredo'
app.config['SECRET_KEY'] = 'segredo'
app.config.from_object("config")

# Inicialização do banco de dados e migração
db = SQLAlchemy(app)
migrate = Migrate(app, db)


lm = LoginManager()
lm.init_app(app)


from app.controllers import home
from app.models import tables

# Definindo o comando CLI para migrações
@app.cli.command("db_migrate")
def db_migrate():
    """Comando personalizado para gerenciar migrações de banco de dados."""
    from flask_migrate import upgrade, migrate, init
    init()
    migrate()
    upgrade()

# Você pode adicionar mais comandos personalizados conforme necessário.

