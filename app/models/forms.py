from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, TelField
from wtforms.validators import DataRequired, Email, ValidationError
from flask import flash
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from app.models.tables import Organizacao, Secao, State, Patente
from app import app  # Certifique-se de que o objeto `app` está disponível


def phone_validator(form, field):
    import re
    phone_number = field.data
    # Regex para validar números de telefone no formato E.164
    if not re.match(r'^\+?[1-9]\d{1,14}$', phone_number):
        flash("Insira um número de celular válido.", 'warning')

class LoginForm(FlaskForm):
    organizacao = SelectField("OM", choices=[], validators=[DataRequired()])
    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField('Entrar')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Preenche o campo de patente com dados do banco
        with app.app_context():
            self.organizacao.choices = [
                (om.id, om.name) for om in Organizacao.query.all()
            ]

class RegisterForm(FlaskForm):
    nvls = [('1', 'Usuário'), ('2', 'Fiscal'), ('3', 'Administrador')]

    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    confirm_password = PasswordField("confirmar senha", validators=[ DataRequired()])

    military_id = StringField("id militar", validators=[DataRequired()])
    patente = SelectField("posto/graduação", choices=[], validators=[DataRequired()])
    nome_completo = StringField("nome completo", validators=[DataRequired()])
    organization = SelectField("posto/graduação", choices=[], validators=[DataRequired()])
    secao = SelectField("Seção", choices=[], validators=[DataRequired()])

    data_nascimento = DateField("data de nascimento", format='%d-%m-%Y', validators=[DataRequired()], render_kw={
            'max': (date.today() - relativedelta(years=19)).strftime('%d-%m-%Y'),  # Máximo: data atual
            'min': (date.today() - relativedelta(years=130)).strftime('%d-%m-%Y')  # Mínimo: 100 anos atrás
        })
    nivel = SelectField("nivel", choices=nvls, validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    telefone = TelField("telefone")
    submit = SubmitField('Registrar')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Preenche o campo de patente com dados do banco
        with app.app_context():
            self.patente.choices = [
                (patente.id, patente.posto) for patente in Patente.query.all()
            ]
            self.organization.choices = [
                (om.id, om.name) for om in Organizacao.query.all()
            ]
            self.secao.choices = [
                (secao.id, secao.section) for secao in Secao.query.all()
            ]

class VacationForm(FlaskForm):

    data_inicio = DateField(
        "Data de Início",
        format='%d-%m-%Y',
        validators=[DataRequired()],
        render_kw={
            'min': (date.today() + timedelta(days=1)).strftime('%d-%m-%Y'),
            'max': date(date.today().year, 12, 31).strftime('%d-%m-%Y')
        }
    )
    data_fim = DateField(
    "Data de Fim",
    format='%d-%m-%Y',
    validators=[DataRequired()],
    render_kw={
        'min': (date.today() + timedelta(days=2)).strftime('%d-%m-%Y'),  # Garantir que a data de fim seja pelo menos 1 dia após a de início
        'max': date(date.today().year, 12, 31).strftime('%d-%m-%Y')  # Máximo: 31 de dezembro de 2025
    }
)
    
    destino = StringField("destino", validators=[DataRequired()])
    motivo = TextAreaField("Motivo")
    detalhes = StringField("detalhes")

    def validate_data_fim(self, field):
        if self.data_inicio.data and field.data < self.data_inicio.data:
            raise ValidationError("A data de fim não pode ser menor que a data de início.")
    
    def validate_max_dias(self, field):
        if self.data_inicio.data and self.data_fim.data:
            delta = (self.data_fim.data - self.data_inicio.data).days
            if delta > field.data:
                raise ValidationError("A quantidade de dias excede os disponíveis para o usuário.")
