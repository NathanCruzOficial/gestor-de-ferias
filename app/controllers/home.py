from app import app, lm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.forms import LoginForm, RegisterForm    
from app.models.tables import Users


@lm.user_loader
def load_user(session_token):
    return Users.query.filter_by(session_token=session_token).first()

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
            flash("Logado")
        else:
            flash("Usuário Inválido")

    else:
        print("error")

    return render_template('login_page.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        ...
    return render_template('registrador.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))