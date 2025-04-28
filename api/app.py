from flask import Flask, jsonify, request, session
from api.routes import criar_usuario, get_usuario, att_usuario, salvar_atividade
from backend.validar_documentos import validar_documento
from backend.googlelogin import login_google, auth_callback, init_google_oauth, oauth, login_data
import os
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'senha_secreta')

#Cria o objeto oauth do google
init_google_oauth(app)
@app.route('/')
def index():
    return "API rodando com Flask!"

@app.route('/api/usuario/<string:usuario_email>', methods=['GET'])
def api_get_usuario(usuario_email):
    # Chama a função para buscar por email
    return get_usuario(usuario_email)

@app.route('/api/usuario', methods=['POST'])
def api_criar_usuario():
    # Chama a função que cria (ou atualiza) o usuário
    return criar_usuario()

@app.route('/api/atualizar_usuario', methods=['POST'])
def api_attusuario():
    return att_usuario()

@app.route('/api/validar_documento', methods=['POST'])
def validar_identidade():
    # Verifica se o documento foi enviado
    if 'documento' not in request.files:
        print("nao teve documento")
        return jsonify({"error": "Nenhum arquivo enviado."}), 400
    
    # Verifica se o CPF foi enviado 
    if 'cpf' not in request.form:
        print("não teve cpf")
        return jsonify({"error": "CPF não informado."}), 400

    documento = request.files['documento']
    cpf = request.form['cpf']

    return validar_documento(documento, cpf)

# rota de login dispara o redirect pro Google
@app.route('/auth/login')
def auth_login():
    return login_google()

# rota de callback recebe o código e processa o token
@app.route('/auth/callback')
def auth_callback_route():
    return auth_callback()

# rota responsavel por devolver as credencias para o frontend
@app.route('/auth/credentials', methods=['GET'])
def get_credentials():
    return login_data()

@app.route('/api/activities', methods=['POST'])
def att_activities():
    return salvar_atividade()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


