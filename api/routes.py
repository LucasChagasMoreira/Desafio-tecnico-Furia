import os
import csv
from flask import jsonify, request, session
from backend.googlelogin import oauth
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
    csv_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'dados', 'dados.csv'
    )

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
    

def buscar_usuario_por_email(email_target, arquivo_csv="dados/dados.csv"):
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
    

