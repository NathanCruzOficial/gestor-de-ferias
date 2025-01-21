from app import app,lm
from app.models.tables import User
from app.routes.user import user_bp
from app.routes.auth import auth_bp


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/')


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))