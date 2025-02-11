from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, TelField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
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
    fg_organization_id = SelectField("OM", choices=[], validators=[DataRequired()])
    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField('Entrar')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Preenche o campo de patente com dados do banco
        with app.app_context():
            self.fg_organization_id.choices = [
                (om.id, om.name) for om in Organizacao.query.all()
            ]

class RegisterForm(FlaskForm):
    nvls = [('1', 'Usuário'), ('2', 'Fiscal'), ('3', 'Administrador')]

    nome_guerra = StringField("nome_guerra", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    confirm_password = PasswordField("confirmar senha", validators=[ DataRequired()])

    military_id = StringField("id militar", validators=[DataRequired()])
    fg_patente_id = SelectField("patente", choices=[], validators=[DataRequired()])
    nome_completo = StringField("nome completo", validators=[DataRequired()])
    fg_organization_id = SelectField("Organização", choices=[], validators=[DataRequired()])
    fg_secao_id = SelectField("Seção", choices=[], validators=[DataRequired()])

    data_nascimento = DateField("data de nascimento", format='%Y-%m-%d', validators=[DataRequired()], render_kw={
            'max': (date.today() - relativedelta(years=19)).strftime('%Y-%m-%d'),  # Máximo: data atual
            'min': (date.today() - relativedelta(years=130)).strftime('%Y-%m-%d')  # Mínimo: 100 anos atrás
        })
    nivel = SelectField("nivel", choices=nvls, validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    telefone = TelField("telefone",validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Preenche o campo de patente com dados do banco
        with app.app_context():
            self.fg_patente_id.choices = [
                (patente.id, patente.posto) for patente in Patente.query.all()
            ]
            self.fg_organization_id.choices = [
                (om.id, om.name) for om in Organizacao.query.all()
            ]
            self.fg_secao_id.choices = [
                (secao.id, secao.section) for secao in Secao.query.all()
            ]
            

class UpdateForm(FlaskForm):
    nvls = [('1', 'Usuário'), ('2', 'Fiscal'), ('3', 'Administrador')]

    nome_guerra = StringField("nome_guerra", validators=[DataRequired()])

    military_id = StringField("id militar", validators=[DataRequired()])
    fg_patente_id = SelectField("patente", choices=[], validators=[DataRequired()])
    nome_completo = StringField("nome completo", validators=[DataRequired()])
    fg_organization_id = SelectField("Organização", choices=[], validators=[DataRequired()])
    fg_secao_id = SelectField("Seção", choices=[], validators=[DataRequired()])

    dias_disp = IntegerField("Dias de Dispensa", default=0)

    data_nascimento = DateField("data de nascimento", format='%Y-%m-%d', validators=[DataRequired()], render_kw={
            'max': (date.today() - relativedelta(years=19)).strftime('%Y-%m-%d'),  # Máximo: data atual
            'min': (date.today() - relativedelta(years=130)).strftime('%Y-%m-%d')  # Mínimo: 100 anos atrás
        })
    nivel = SelectField("nivel", choices=nvls, validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    telefone = TelField("telefone",validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        # Preenche o campo de patente com dados do banco
        with app.app_context():
            self.fg_patente_id.choices = [
                (patente.id, patente.posto) for patente in Patente.query.all()
            ]
            self.fg_organization_id.choices = [
                (om.id, om.name) for om in Organizacao.query.all()
            ]
            self.fg_secao_id.choices = [
                (secao.id, secao.section) for secao in Secao.query.all()
            ]
            

class VacationForm(FlaskForm):
    periodo_dias = [('1', '30 dias'), ('2', '25 dias'), ('3', '20 dias'), ('4', '15 dias'), ('4', '10 dias'),('4', '5 dias')]

    data_inicio = DateField(
        "Data de Início",
        format='%Y-%m-%d',
        validators=[DataRequired()],
        render_kw={
            'min': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'max': date(date.today().year, 12, 31).strftime('%Y-%m-%d')
        }
    )

    periodo = SelectField("Período", choices=periodo_dias, validators=[DataRequired()])

    destino = StringField("Destino", validators=[DataRequired()])
    motivo = TextAreaField("Motivo")
    detalhes = StringField("Detalhes")
    submit = SubmitField('Salvar')

    def validate_data_fim(self, field):
        if self.data_inicio.data and field.data < self.data_inicio.data:
            raise ValidationError("A data de fim não pode ser menor que a data de início.")
    
    def validate_max_dias(self, field):
        if self.data_inicio.data and self.data_fim.data:
            delta = (self.data_fim.data - self.data_inicio.data).days
            if delta > field.data:
                raise ValidationError("A quantidade de dias excede os disponíveis para o usuário.")
            
class ProfileForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    telefone = TelField("telefone",validators=[DataRequired()])
    submit = SubmitField('Salvar')

class PasswordChangeForm(FlaskForm):
    senha_atual = PasswordField("Senha Atual")
    nova_senha = PasswordField("Nova Senha", validators=[DataRequired()])
    confirmar_senha = PasswordField("Confirme a Nova Senha", validators=[DataRequired(), EqualTo('nova_senha')])
    submit = SubmitField('Enviar')

# Formulário para solicitar código de recuperação
class ResetPasswordForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar Código")

# Formulário para validar código
class VerifyCodeForm(FlaskForm):
    codigo = StringField("Código de Verificação", validators=[DataRequired()])
    submit = SubmitField("Validar Código")

# Formulário para redefinir a senha
class NewPasswordForm(FlaskForm):
    nova_senha = PasswordField("Nova Senha", validators=[DataRequired()])
    confirmar_senha = PasswordField("Confirme a Nova Senha", validators=[DataRequired(), EqualTo('nova_senha')])
    submit = SubmitField("Alterar Senha")

