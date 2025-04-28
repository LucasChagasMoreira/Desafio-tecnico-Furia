# backend/googlelogin.py

from authlib.integrations.flask_client import OAuth
from flask import url_for, session, redirect, make_response
import os
import csv
import json
oauth = OAuth()  

def init_google_oauth(app):
    app.config['GOOGLE_CLIENT_ID']     = '1038201317836-g08gjvqlsdaeoi3qtnpjh49i0cm24u3i.apps.googleusercontent.com'
    app.config['GOOGLE_CLIENT_SECRET'] = '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'
    oauth.init_app(app) 
    oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        client_kwargs={'scope': 'openid email profile'},
    )

def login_google():
    # Instancia o cliente ja criado
    client = oauth.create_client('google') 
    redirect_uri = url_for('auth_callback_route', _external=True)
    return client.authorize_redirect(redirect_uri)

def auth_callback():
    # troca o código por token e salva na sessão
    client = oauth.create_client('google')
    token = client.authorize_access_token()
    session['oauth_token'] = token

    # decodifica o ID Token (com nonce salvo)
    nonce = session.get(f'oauth_{client.name}_nonce')
    user_info = client.parse_id_token(token, nonce)

    # armazena o perfil do usuário na sessão
    session['user'] = {
        'id': user_info['sub'],
        'name': user_info['name'],
        'email': user_info['email'],
        'picture': user_info.get('picture', '')
    }

    # grava no CSV apenas se email não existe
    csv_file = 'dados/dados.csv'
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    fieldnames = ['Nome', 'Email', 'CPF', 'Endereço']
    user_email = user_info.get('email', '')
    user_name = user_info.get('name', '')

    # Verifica existência
    exists = False
    if os.path.isfile(csv_file):
        try:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Email') == user_email:
                        exists = True
                        break
        except Exception as e:
            print(f'Erro ao ler CSV: {e}')

    # Se não existe, adiciona nova linha
    if not exists:
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if os.stat(csv_file).st_size == 0:
                    writer.writeheader()
                writer.writerow({
                    'Nome': user_name,
                    'Email': user_email,
                    'CPF': '',
                    'Endereço': ''
                })
        except Exception as e:
            print(f'Erro ao escrever CSV: {e}')

    # grava um JSON cache para o front
    json_cache = 'backend/auth.json'
    os.makedirs(os.path.dirname(json_cache), exist_ok=True)
    cache_entry = {
        'Nome': user_name,
        'Email': user_email
    }
    try:
        with open(json_cache, 'w', encoding='utf-8') as jf:
            json.dump(cache_entry, jf, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Erro ao salvar JSON cache: {e}')

    return redirect(url_for('index'))


def login_data():

    # Caminho absoluto para o pasta backend
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cache_path = "backend/auth.json"

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {cache_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erro de JSON em {cache_path}: {e}")
        return {}
    except Exception as e:
        print(f"Erro ao ler {cache_path}: {e}")
        return {}

    # Apaga o arquivo após a leitura
    try:
        os.remove(cache_path)
    except Exception as e:
        print(f"Erro ao deletar {cache_path}: {e}")

    return data
