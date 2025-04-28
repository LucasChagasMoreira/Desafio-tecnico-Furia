import json
import csv
import os

def process_json_to_csv(json_path: str, info_csv: str, activities_csv: str):
    """
    Lê um arquivo JSON em `json_path` e grava dois CSVs:
      - `info_csv`: colunas Nome, Email, CPF, Endereço.
      - `activities_csv`: colunas Email, Tipo, Link (somente follow_facebook).
    """
    # Carrega JSON
    with open(json_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    # Garante diretórios
    os.makedirs(os.path.dirname(info_csv), exist_ok=True)
    os.makedirs(os.path.dirname(activities_csv), exist_ok=True)

    # 1) CSV de info do usuário (sem Link do Perfil)
    info_fields = ['Nome', 'Email', 'CPF', 'Endereço']
    info_exists = os.path.isfile(info_csv)
    with open(info_csv, 'a', newline='', encoding='utf-8') as f_info:
        writer = csv.DictWriter(f_info, fieldnames=info_fields)
        if not info_exists:
            writer.writeheader()
        row_info = {
            'Nome': data.get('Nome', ''),
            'Email': data.get('Email', ''),
            'CPF': data.get('CPF', ''),
            'Endereço': data.get('Endereço', '')
        }
        writer.writerow(row_info)

    # 2) CSV de atividades: apenas follow_facebook
    activities_fields = ['Email', 'Tipo', 'Link']
    act_exists = os.path.isfile(activities_csv)
    with open(activities_csv, 'a', newline='', encoding='utf-8') as f_act:
        writer = csv.DictWriter(f_act, fieldnames=activities_fields)
        if not act_exists:
            writer.writeheader()
        email = data.get('Email', '')
        for entry in data.get('follow_facebook', []):
            writer.writerow({
                'Email': email,
                'Tipo': 'follow',
                'Link': entry.get('link', '')
            })

if __name__ == '__main__':
    # Exemplo de uso
    process_json_to_csv(
        json_path='dados/dadosexemplo.json',
        info_csv='dados/dados.csv',
        activities_csv='dados/atividades.csv'
    )
