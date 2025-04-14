from flask import Flask
from routes import criar_usuario, get_usuario

app = Flask(__name__)

@app.route('/')
def index():
    return "API rodando com Flask!"

@app.route('/api/usuario/<string:usuario_email>', methods=['GET'])
def api_get_usuario(usuario_email):
    # Chama a função que busca o usuário pelo email
    return get_usuario(usuario_email)

@app.route('/api/usuario', methods=['POST'])
def api_criar_usuario():
    # Chama a função que cria (ou atualiza) o usuário
    return criar_usuario()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
