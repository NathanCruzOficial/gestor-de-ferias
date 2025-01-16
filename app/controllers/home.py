from app import app, db, lm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models.forms import LoginForm, RegisterForm    
from app.models.tables import Users

@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Página principal
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    # return redirect(url_for('login'))

# # Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username= form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Usuário Inválido")
            return redirect(url_for('login'))

    else:
        print("error")

    return render_template('login_page.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
      # Aqui o registro seria processado.
        username = form.username.data
        password = form.password.data
        nome_completo = form.nome_completo.data
        posto_grad = form.posto_grad.data
        data_nascimento = form.data_nascimento.data
        nivel = form.nivel.data
        email = form.email.data
        telefone = form.telefone.data

        user = Users(username=username, password=password, nome_completo=nome_completo,dias_disp=0, posto_grad=posto_grad, data_nascimento=data_nascimento, nivel=nivel, email=email, telefone=telefone)

        db.session.add(user)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')




    else:
        # Coleta os erros do formulário
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)

    return render_template('registrador.html', form=form)

@app.route('/logout')
def logout():
    logout_user()  # Encerra a sessão do usuário
    return redirect(url_for('login'))