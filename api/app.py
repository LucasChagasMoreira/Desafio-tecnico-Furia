from flask import Flask, jsonify, request
from api.routes import criar_usuario, get_usuario
from backend.validar_documentos import validar_documento

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


@app.route('/api/validar_documento', methods=['POST'])
def validar_identidade():
    if 'documento' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    documento = request.files['documento']
    return validar_documento(documento)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


