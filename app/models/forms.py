from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, ValidationError

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
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    patents = [('1', 'Soldado'),
               ('2', 'Cabo'),
               ('3', '3º Sargento'),
               ('4', '2º Sargento'),
               ('5', '1º Sargento'),
               ('6', 'Sub Tenente'),
               ('7', '2º Tenente'),
               ('8', '1º Tenente'),
               ('9', 'Capitão'),
               ('10', 'Major'),
               ('11', 'Tenente Coronel'),
               ('12', 'Coronel'),
               ('13', 'General de Brigada'),
               ('14', 'General de Divisão'),
               ('15', 'General de Exército')]
    nvls = [('1', '0'), ('2', '1'), ('3', '2')]

    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    patent = SelectField("patent", choices=patents, validators=[DataRequired()])
    all_name = StringField("all_name", validators=[DataRequired()])
    birthday = DateField("birthday", format='%Y-%m-%d', validators=[DataRequired()])
    nivel = SelectField("nivel", choices=nvls, validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    celphone = StringField("celphone", validators=([phone_validator]))
    submit = SubmitField('Login')