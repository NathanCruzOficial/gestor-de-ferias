from app import app
import webview




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    # # Cria uma janela com um título e um site carregado
    # webview.create_window("gestor-ferias", app)

    # # Inicia a aplicação
    # webview.start()