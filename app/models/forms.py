from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, ValidationError
from flask import flash
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

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

def phone_validator(form, field):
    import re
    phone_number = field.data
    # Regex para validar números de telefone no formato E.164
    if not re.match(r'^\+?[1-9]\d{1,14}$', phone_number):
        flash("Insira um número de celular válido.", 'warning')

class LoginForm(FlaskForm):
    posto_grad = SelectField("posto/graduação", choices=patents, validators=[DataRequired()])
    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nvls = [('1', 'Usuário'), ('2', 'Fiscal'), ('3', 'Administrador')]

    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    confirm_password = PasswordField("confirmar senha", validators=[ DataRequired()])

    military_id = StringField("id militar", validators=[DataRequired()])
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

class VacationForm(FlaskForm):

    data_inicio = DateField(
        "Data de Início",
        format='%Y-%m-%d',
        validators=[DataRequired()],
        render_kw={
            'min': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'max': date(date.today().year, 12, 31).strftime('%Y-%m-%d')
        }
    )
    data_fim = DateField(
    "Data de Fim",
    format='%Y-%m-%d',
    validators=[DataRequired()],
    render_kw={
        'min': (date.today() + timedelta(days=2)).strftime('%Y-%m-%d'),  # Garantir que a data de fim seja pelo menos 1 dia após a de início
        'max': date(date.today().year, 12, 31).strftime('%Y-%m-%d')  # Máximo: 31 de dezembro de 2025
    }
)
    
    destino = StringField("destino", validators=[DataRequired()])
    motivo = StringField("Motivo")
    detalhes = StringField("detalhes")

    def validate_data_fim(self, field):
        if self.data_inicio.data and field.data < self.data_inicio.data:
            raise ValidationError("A data de fim não pode ser menor que a data de início.")
    
    def validate_max_dias(self, field):
        if self.data_inicio.data and self.data_fim.data:
            delta = (self.data_fim.data - self.data_inicio.data).days
            if delta > field.data:
                raise ValidationError("A quantidade de dias excede os disponíveis para o usuário.")
