from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

def phone_validator(form, field):
    import re
    phone_number = field.data
    # Regex para validar números de telefone no formato E.164
    if not re.match(r'^\+?[1-9]\d{1,14}$', phone_number):
        raise ValidationError("Insira um número de celular válido.")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    patents = [('Soldado', 'Soldado'),
    ('Cabo', 'Cabo'),
    ('3º Sargento', '3º Sargento'),
    ('2º Sargento', '2º Sargento'),
    ('1º Sargento', '1º Sargento'),
    ('Sub Tenente', 'Sub Tenente'),
    ('2º Tenente', '2º Tenente'),
    ('1º Tenente', '1º Tenente'),
    ('Capitão', 'Capitão'),
    ('Major', 'Major'),
    ('Tenente Coronel', 'Tenente Coronel'),
    ('Coronel', 'Coronel'),
    ('General de Brigada', 'General de Brigada'),
    ('General de Divisão', 'General de Divisão'),
    ('General de Exército', 'General de Exército')]
    nvls = [('1', '1'), ('2', '2'), ('3', '3')]

    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    posto_grad = SelectField("posto/graduação", choices=patents, validators=[DataRequired()])
    nome_completo = StringField("nome completo", validators=[DataRequired()])
    data_nascimento = DateField("data de nascimento", format='%Y-%m-%d', validators=[DataRequired()], render_kw={
            'max': (date.today() - relativedelta(years=19)).strftime('%Y-%m-%d'),  # Máximo: data atual
            'min': (date.today() - relativedelta(years=130)).strftime('%Y-%m-%d')  # Mínimo: 100 anos atrás
        })
    nivel = SelectField("nivel", choices=nvls, validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    telefone = StringField("telefone", validators=([phone_validator]))
    submit = SubmitField('Registrar')