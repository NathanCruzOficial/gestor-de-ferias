from flask import Flask, send_file
from docx import Document

app = Flask(__name__)

def preencher_docx(modelo_path, dados, tabela_dados, output_path):
    """Preenche um documento Word com dados e adiciona linhas dinamicamente em uma tabela."""
    doc = Document(modelo_path)

    # Substituir placeholders nos parágrafos
    for paragrafo in doc.paragraphs:
        for chave, valor in dados.items():
            if f"{{{{{chave}}}}}" in paragrafo.text:
                paragrafo.text = paragrafo.text.replace(f"{{{{{chave}}}}}", valor)

    # Encontrar a tabela e preencher com os dados dinâmicos
    for tabela in doc.tables:
        if len(tabela.rows) == 1:  # Garante que a tabela tenha apenas o cabeçalho inicialmente
            for item in tabela_dados:
                linha = tabela.add_row().cells
                linha[0].text = item["codigo"]
                linha[1].text = item["descricao"]
                linha[2].text = str(item["quantidade"])

    doc.save(output_path)

@app.route('/gerar-relatorio')
def gerar_relatorio():
    modelo_path = "modelos/modelo.docx"
    output_path = "documentos_gerados/relatorio_preenchido.docx"

    # Dados fixos
    dados = {
        "NOME": "João Silva",
        "DATA": "29/01/2025"
    }

    # Dados dinâmicos da tabela
    tabela_dados = [
        {"codigo": "A001", "descricao": "Produto X", "quantidade": 10},
        {"codigo": "A002", "descricao": "Produto Y", "quantidade": 5},
        {"codigo": "A003", "descricao": "Produto Z", "quantidade": 8},
        {"codigo": "A004", "descricao": "Produto W", "quantidade": 15},  # Adicione quantas linhas quiser
    ]

    # Gerar documento
    preencher_docx(modelo_path, dados, tabela_dados, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
