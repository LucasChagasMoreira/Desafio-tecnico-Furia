import os
import json
import csv

def fake_data(json_path, info_csv, activities_csv):
    # Carrega JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        raise ValueError(f"Falha ao ler JSON: {e}")

    # Extrai info para retorno e CSV
    info = {
        'Nome': data.get('Nome', ''),
        'Email': data.get('Email', ''),
        'CPF': data.get('CPF', ''),
        'Endereço': data.get('Endereço', '')
    }

    # Garante diretórios
    os.makedirs(os.path.dirname(info_csv), exist_ok=True)
    os.makedirs(os.path.dirname(activities_csv), exist_ok=True)

    # 1) Grava info_csv (Nome, Email, CPF, Endereço)
    info_fields = ['Nome', 'Email', 'CPF', 'Endereço']
    exists_info = os.path.isfile(info_csv)
    with open(info_csv, 'a', newline='', encoding='utf-8') as f_info:
        writer = csv.DictWriter(f_info, fieldnames=info_fields)
        if not exists_info:
            writer.writeheader()
        writer.writerow(info)

    # 2) Grava activities_csv (Email, Tipo=follow, Link)
    activity_fields = ['Email', 'Tipo', 'Link']
    exists_act = os.path.isfile(activities_csv)
    with open(activities_csv, 'a', newline='', encoding='utf-8') as f_act:
        writer = csv.DictWriter(f_act, fieldnames=activity_fields)
        if not exists_act:
            writer.writeheader()
        email = info['Email']
        for entry in data.get('follow_facebook', []):
            writer.writerow({
                'Email': email,
                'Tipo': 'follow',
                'Link': entry.get('link', '')
            })

    return info
