import os
import csv
from flask import jsonify, request
import threading

DADOS_PATH = 'dados/dados.csv'
ATIVIDADES_PATH = 'dados/atividades.csv'

def get_usuario(usuario_email):
    # Busca no CSV o usuário com o email informado
    usuario = buscar_usuario_por_email(usuario_email)
    if usuario:
        return jsonify(usuario), 200
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

def criar_usuario():
    data = request.get_json()
    # Verifica se os campos necessários estão presentes
    if not data or not all(key in data for key in ("Nome", "Email")):
        return jsonify({"error": "Dados incompletos"}), 400

    # Constrói o caminho para o arquivo CSV relativo à raiz do projeto
    csv_filename = DADOS_PATH

    try:
        # verifica a existencia do arquivo e seu conteudo
        file_exists = os.path.exists(csv_filename) and os.stat(csv_filename).st_size > 0

        with open(csv_filename, "a", encoding="utf-8", newline="") as arquivo:
            writer = csv.writer(arquivo)
            if not file_exists:

                writer.writerow(["Nome", "Email", "CPF", "Endereço"])
            # Escreve os dados recebidos e insere dois campos vazios para CPF e Endereço
            writer.writerow([
                data["Nome"],
                data["Email"],
                " ",  
                " "   
            ])

        return jsonify({
            "Nome": data["Nome"],
            "Email": data["Email"],
            "CPF": " ",
            "Endereço": " "
        }), 201

    except Exception as e:
        print("Erro ao salvar os dados:", e)
        return jsonify({"error": "Erro no servidor"}), 500
    

def buscar_usuario_por_email(email_target, arquivo_csv=DADOS_PATH):
    try:
        with open(arquivo_csv, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Assume que a coluna do email está com o cabeçalho "Email"
                if row.get("Email", "").strip().lower() == email_target.lower():
                    return row
        return None
    except Exception as e:
        print("Erro ao abrir o arquivo:", e)
        return None

def salvar_atividade():
    data = request.get_json(force=True)
    email = data.get('Email')
    link = data.get('link')
    CSV_LOCK = threading.Lock()
    USERS_CSV = DADOS_PATH
    ACTIVITIES_CSV = ATIVIDADES_PATH

    if not email or not link:
        return jsonify({'error': 'Dados incompletos'}), 400

    with CSV_LOCK:
        # Verifica existência do email no CSV de usuários
        try:
            with open(USERS_CSV, newline='', encoding='utf-8') as f_users:
                reader = csv.DictReader(f_users)
                if 'Email' not in reader.fieldnames:
                    return jsonify({'error': 'Coluna Email não encontrada no CSV de usuários'}), 500

                exists = any(row['Email'] == email for row in reader)
        except FileNotFoundError:
            return jsonify({'error': 'CSV de usuários não encontrado'}), 500
        except Exception as e:
            return jsonify({'error': f'Erro ao ler CSV de usuários: {e}'}), 500

        if not exists:
            return jsonify({'error': 'Email não cadastrado'}), 404

        # Prepara atividade
        activity = {
            'Email': email,
            'tipo': 'acesso',
            'link': link
        }

        # Escreve no CSV de atividades
        file_exists = os.path.isfile(ACTIVITIES_CSV)
        try:
            with open(ACTIVITIES_CSV, 'a', newline='', encoding='utf-8') as f_act:
                fieldnames = ['Email','tipo', 'link']
                writer = csv.DictWriter(f_act, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(activity)
        except Exception as e:
            return jsonify({'error': f'Falha ao gravar atividades: {e}'}), 500

    return jsonify({'status': 'Atividade registrada'}), 200
  
def att_usuario():
    # Extrai dados do corpo da requisição
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Corpo JSON inválido'}), 400

    email = data.get('Email')
    if not email:
        return jsonify({'error': 'Campo "email" é obrigatório'}), 400

    filepath = DADOS_PATH

    # 2) Lê todas as linhas do CSV
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo CSV não encontrado'}), 500

    # 3) Procura e atualiza a linha do usuário
    updated = False
    for row in rows:
        if row.get('Email') == email:
            # atualiza só os campos que existem no CSV
            for key, value in data.items():
                if key in fieldnames:
                    row[key] = value
            updated = True
            break

    if not updated:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    # 4) Escreve de volta todas as linhas, com header
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        return jsonify({'error': f'Falha ao gravar CSV: {e}'}), 500

    # 5) Retorna sucesso
    return jsonify({
        'status': 'sucesso',
        'updated': {
            'email': email,
            **{k: v for k, v in data.items() if k in fieldnames}
        }
    }), 200


