from app import app
from flask import render_template, request, redirect, url_for, session
# from datetime import datetime

# # Dados simulados
clientes = [
    {'username': 'cliente1', 'password': '1234', 'posto': 'Soldado', 'nome': 'João Silva', 'dias_disponiveis': 60, 'historico': [
        {'tipo': 'retirado', 'dias': 30, 'data': '05/maio/2022'},
        {'tipo': 'recebido', 'dias': 30, 'data': '01/jan/2022'},
        {'tipo': 'retirado', 'dias': 15, 'data': '23/nov/2022'},
        {'tipo': 'retirado', 'dias': 15, 'data': '16/fev/2022'},
        {'tipo': 'recebido', 'dias': 30, 'data': '01/jan/2021'},
    ]}
]

ferias = []

admins = [
    {'username': 'admin1', 'password': '1234', 'nivel': 2},
    {'username': 'admin2', 'password': '1234', 'nivel': 1},
    {'username': 'admin3', 'password': '1234', 'nivel': 0},
]

# Página principal
@app.route('/')
@app.route('/index')
def index():
    if 'user' in session:
        for cliente in clientes:
            if cliente['username'] == session['user']:
                return render_template('home.html', cliente=cliente, ferias=ferias)
    return redirect(url_for('login'))

# # Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for cliente in clientes:
            if cliente['username'] == username and cliente['password'] == password:
                session['user'] = username
                return redirect(url_for('index'))
        return "Login falhou. Verifique suas credenciais."

    return render_template('login_page.html')

# # Registrar férias
# @app.route('/registrar', methods=['POST'])
# def registrar_ferias():
#     if 'user' in session:
#         inicio = request.form['inicio']
#         fim = request.form['fim']
#         destino = request.form['destino']

#         for cliente in clientes:
#             if cliente['username'] == session['user']:
#                 data_inicio = datetime.strptime(inicio, '%Y-%m-%d')
#                 data_fim = datetime.strptime(fim, '%Y-%m-%d')
#                 dias = (data_fim - data_inicio).days + 1

#                 if cliente['dias_disponiveis'] >= dias:
#                     cliente['dias_disponiveis'] -= dias
#                     cliente['historico'].append({'tipo': 'retirado', 'dias': dias, 'data': datetime.now().strftime('%d/%b/%Y')})
#                     ferias.append({'inicio': inicio, 'fim': fim, 'destino': destino, 'cliente': cliente['username']})
#                     return render_template('ferias_registradas.html', ferias=ferias[-1])
#                 else:
#                     return "Você não tem dias suficientes para registrar essas férias."

#     return redirect(url_for('login_cliente'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    session.pop('nivel', None)
    return redirect(url_for('login'))


# # Página de login do administrador
# @app.route('/login_admin', methods=['GET', 'POST'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         for admin in admins:
#             if admin['username'] == username and admin['password'] == password:
#                 session['admin'] = username
#                 session['nivel'] = admin['nivel']
#                 return redirect(url_for('admin_area'))
#         return "Login falhou. Verifique suas credenciais."

#     return render_template('login_admin.html')

# # Área administrativa
# @app.route('/admin_area')
# def admin_area():
#     if 'admin' in session:
#         nivel = session['nivel']
        
#         # Administrador nível 2 pode acessar tudo
#         if nivel == 2:
#             return render_template('nivel_2.html', ferias=ferias, admins=admins)
        
#         # Administrador nível 1 pode acessar nível 1 e 0
#         elif nivel == 1:
#             return render_template('nivel_1.html', ferias=ferias, admins=admins)

#         # Administrador nível 0
#         elif nivel == 0:
#             return render_template('nivel_0.html', ferias=ferias)
    
#     return redirect(url_for('login_admin'))

# # Adicionar administrador
# @app.route('/adicionar_admin', methods=['POST'])
# def adicionar_admin():
#     if 'admin' in session and session['nivel'] == 2:
#         username = request.form['username']
#         password = request.form['password']
#         nivel = int(request.form['nivel'])
        
#         # Administrador nível 2 pode adicionar qualquer nível de administrador
#         admins.append({'username': username, 'password': password, 'nivel': nivel})
#         return redirect(url_for('admin_area'))
    
#     # Verificação para permitir adicionar administradores de nível 1 para o nível 0
#     if 'admin' in session and session['nivel'] == 1:
#         username = request.form['username']
#         password = request.form['password']
#         admins.append({'username': username, 'password': password, 'nivel': 0})
#         return redirect(url_for('admin_area'))
    
#     return redirect(url_for('login_admin'))

# # Deletar administrador
# @app.route('/deletar_admin/<username>')
# def deletar_admin(username):
#     if 'admin' in session:
#         global admins
#         nivel = session['nivel']
        
#         # Administrador nível 2 pode deletar qualquer administrador
#         if nivel == 2:
#             admins = [admin for admin in admins if admin['username'] != username]
#             return redirect(url_for('admin_area'))

#         # Administrador nível 1 pode deletar administradores de nível 0
#         if nivel == 1:
#             admins = [admin for admin in admins if admin['username'] != username and admin['nivel'] == 0]
#             return redirect(url_for('admin_area'))
    
#     return redirect(url_for('login_admin'))