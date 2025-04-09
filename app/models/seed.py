from app.models.tables import User, Organizacao, Secao, State, Patente
from app import db

from datetime import datetime

# Obtém a data de hoje
data_nascimento_str = '2001-06-12'
data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

def seed_data():
    # Dados iniciais para a tabela Organization
    organizations = [
        {"abrev": "Companhia", "name": "Cia C GUEs - 9ª Bda Inf Mtz"},
        {"abrev": "Comando", "name": "GUEs - 9ª Bda Inf Mtz"},
        {"abrev": "Pel PE", "name": "9º Pel PE"}
    ]

    # Usa merge para cada registro, sem passar o id
    for org_data in organizations:
        org = Organizacao(**org_data)
        db.session.merge(org)  # Atualiza ou insere

    # Dados iniciais para a tabela Section
    sections = [
    {"section": "Cmt Bda", "email": "cmt@9bdainfmtz.eb.mil.br"},
    {"section": "Ch EM", "email": "chem@9bdainfmtz.eb.mil.br"},
    {"section": "Od", "email": "od@9bdainfmtz.eb.mil.br"},
    {"section": "Asse Ges", "email": "asseges@9bdainfmtz.eb.mil.br"},
    {"section": "E1", "email": "e1@9bdainfmtz.eb.mil.br"},
    {"section": "E2", "email": "e2@9bdainfmtz.eb.mil.br"},
    {"section": "E3", "email": "e3@9bdainfmtz.eb.mil.br"},
    {"section": "E4", "email": "e4@9bdainfmtz.eb.mil.br"},
    {"section": "E5", "email": "e5@9bdainfmtz.eb.mil.br"},
    {"section": "Com Soc", "email": "comsoc@9bdainfmtz.eb.mil.br"},
    {"section": "Ajg", "email": "ajg@9bdainfmtz.eb.mil.br"},
    {"section": "Ass Jur", "email": "assjur@9bdainfmtz.eb.mil.br"},
    {"section": "Salc", "email": "salc@9bdainfmtz.eb.mil.br"},
    {"section": "Adj Cmdo", "email": "adjcmdo@9bdainfmtz.eb.mil.br"},
    {"section": "Gab Cmt", "email": "gabcmt@9bdainfmtz.eb.mil.br"},
    {"section": "Prm", "email": "prm@9bdainfmtz.eb.mil.br"},
    {"section": "Fisc Adm", "email": "fiscadm@9bdainfmtz.eb.mil.br"},
    {"section": "Cia C", "email": "ciac@9bdainfmtz.eb.mil.br"},
    {"section": "9º Pel PE", "email": "9pelpe@9bdainfmtz.eb.mil.br"},
    {"section": "Almox", "email": "almox@9bdainfmtz.eb.mil.br"},
    {"section": "Capelania", "email": "capl@9bdainfmtz.eb.mil.br"},
    {"section": "Setfin", "email": "setfin@9bdainfmtz.eb.mil.br"},
    {"section": "Sup Doc", "email": "supdoc@9bdainfmtz.eb.mil.br"},
    {"section": "Conformidade", "email": "conformidade@9bdainfmtz.eb.mil.br"},
    {"section": "Spp", "email": "spp@9bdainfmtz.eb.mil.br"},
    {"section": "SeçInfor", "email": "secinfor@9bdainfmtz.eb.mil.br"},
    {"section": "E10", "email": "e10@9bdainfmtz.eb.mil.br"},
    {"section": "Orgão de Inteligência", "email": "escritorio@9bdainfmtz.eb.mil.br"},
    {"section": "Ch Orgão de Inteligência1", "email": "escritorio.ch@9bdainfmtz.eb.mil.br"},
    {"section": "Aprov", "email": "aprov@9bdainfmtz.eb.mil.br"}
]

    for sec_data in sections:
        print(sec_data)  # Verifique os dados antes da inserção
        sec = Secao(**sec_data)
        db.session.merge(sec)  # Atualiza ou insere

    # Dados iniciais para a tabela Patente
    graduacao = [
        {"abrev": "SD", "posto": "Soldado"},
        {"abrev": "CB", "posto": "Cabo"},
        {"abrev": "SGT", "posto": "3º Sargento"},
        {"abrev": "SGT", "posto": "2º Sargento"},
        {"abrev": "SGT", "posto": "1º Sargento"},
        {"abrev": "ST", "posto": "Sub Tenente"},
        {"abrev": "TEN", "posto": "2º Tenente"},
        {"abrev": "TEN", "posto": "1º Tenente"},
        {"abrev": "CAP", "posto": "Capitão"},
        {"abrev": "MAJ", "posto": "Major"},
        {"abrev": "TC", "posto": "Tenente Coronel"},
        {"abrev": "CEL", "posto": "Coronel"},
        {"abrev": "GEN BDA", "posto": "General de Brigada"},
        {"abrev": "GEN DIV", "posto": "General de Divisão"},
        {"abrev": "GEN EX", "posto": "General de Exército"}
    ]
    for rank_data in graduacao:
        rank = Patente(**rank_data)
        db.session.merge(rank)  # Atualiza ou insere

    # Dados iniciais para a tabela State
    stats = [
        {"abrev": "analise", "desc": "EM ANÁLISE"},
        {"abrev": "aprovada", "desc": "APROVADO"},
        {"abrev": "reprovada", "desc": "REPROVADO"},
        {"abrev": "expirada", "desc": "EXPIRADO"},
        {"abrev": "consumindo", "desc": "EM ANDAMENTO"},
        {"abrev": "finalizado", "desc": "FINALIZADO"}  # Corrigido ID duplicado
    ]
    for stat_data in stats:
        stat = State(**stat_data)
        db.session.merge(stat)  # Atualiza ou insere

    # Dados iniciais para a tabela User
    users = [
        {
            "username":"ADMIN",
            "password": "1234",  # Você pode armazenar uma hash da senha usando bcrypt ou similar
            "military_id": "123456789",
            "fg_patente_id": 1,  # Relacionado ao ID da patente (exemplo: Soldado = 1)
            "nome_completo": "ADMIN",
            "nome_guerra": "ADMIN",
            "fg_organization_id": 2,  # Relacionado ao ID da organização (exemplo: "GUEs - 9ª Bda Inf Mtz")
            "fg_secao_id": 26,  # Relacionado ao ID da seção
            "data_nascimento": data_nascimento,  # Formato string para facilitar conversão posterior
            "nivel": 3,  # 3 representa "Administrador"
            "dias_disp": 0,
            "email": "secinfor@9bdainfmtz.eb.mil.br",
            "telefone": "00000000000"
        }
    ]
    for user_data in users:
        user = User(**user_data)
        db.session.merge(user)  # Atualiza ou insere

    db.session.commit()
    print("Dados iniciais foram adicionados ou atualizados com sucesso!")