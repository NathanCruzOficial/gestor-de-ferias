from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.controllers import db_mannager
from app.models.tables import User
from app.models.forms import ResetPasswordForm, VerifyCodeForm, NewPasswordForm
import random
from mailersend import emails

# Configuração do MailerSend
API_KEY = "mlsn.4d2b1b378a971b5e0bc56b83d7afaf90f17dab68453f524880d0c188e1342f7d"
# API_KEY = "mlsn.ea6b1a42eb11f487892e1f003c41661864559e08048f434372563bc163b9de3f"
# Cria o cliente de API do MailerSend
mailer = emails.NewEmail(API_KEY)

reset_bp = Blueprint("reset", __name__)

# 📌 Rota para solicitar o código de recuperação
@reset_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        
        if user:
            codigo = str(random.randint(100000, 999999))  # Gera código de 6 dígitos
            session['codigo_recuperacao'] = codigo
            session['email_recuperacao'] = email

            print(codigo)

            # define an empty dict to populate with mail values
            mail_body = {}

            mail_from = {
                "name": "no-reply",
                "email": "MS_2g1ZZ4@trial-0p7kx4xz5p2g9yjr.mlsender.net",
            }

            recipients = [
                {
                    "name": user.nome_guerra,
                    "email": user.email,
                }
            ]

            personalization = [
                {
                    "email": user.email,
                    "data": {
                        "code": codigo,
                        "name": user.nome_guerra
                    }
                }
            ]

            mailer.set_mail_from(mail_from, mail_body)
            mailer.set_mail_to(recipients, mail_body)
            mailer.set_subject("Recuperar Senha", mail_body)
            mailer.set_template("zr6ke4n7r53gon12", mail_body)
            mailer.set_personalization(personalization, mail_body)

            print(mailer.send(mail_body))

            flash("Código enviado para seu e-mail.", "success")
            return redirect(url_for('reset.validar_codigo'))
        else:
            flash("Não existe usuário com este E-mail!", "danger")

    return render_template('auth/recuperar_senha.html', form=form)

# 📌 Rota para validar o código
@reset_bp.route('/validar-codigo', methods=['GET', 'POST'])
def validar_codigo():
    form = VerifyCodeForm()
    if form.validate_on_submit():
        codigo_digitado = form.codigo.data
        codigo_correto = session.get('codigo_recuperacao')

        if codigo_digitado == codigo_correto:
            flash("Código válido! Redefina sua senha.", "success")
            return redirect(url_for('reset.nova_senha'))
        else:
            flash("Código inválido!", "danger")

    return render_template('auth/validar_codigo.html', form=form)

# 📌 Rota para redefinir a senha
@reset_bp.route('/nova-senha', methods=['GET', 'POST'])
def nova_senha():
    form = NewPasswordForm()
    if form.validate_on_submit():
        email = session.get('email_recuperacao')
        user = User.query.filter_by(email=email).first()

        if user:
            user.set_password(form.nova_senha.data)  # Define a nova senha
            db_mannager.db_update(user)
            flash("Senha alterada com sucesso! Faça login.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Erro ao alterar a senha!", "danger")

    return render_template('auth/nova_senha.html', form=form)
