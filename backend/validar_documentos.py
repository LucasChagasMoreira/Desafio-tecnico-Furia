import pytesseract
from PIL import Image
from flask import jsonify, request

def validar_documento(documento, cpf):
    try:
        # Abre a imagem do arquivo enviado
        image = Image.open(documento.stream)
        
        # Extrai o texto da imagem (ajuste o idioma conforme necessário)
        texto_extraido = pytesseract.image_to_string(image, lang='por')
        
        if cpf in texto_extraido:
            return jsonify({
                "valid": True,
                "message": "CPF encontrado no documento.",
                "texto": texto_extraido
            }), 200
        else:
            print("cpf não contido")
            return jsonify({
                "valid": False,
                "message": "CPF não encontrado no documento.",
                "texto": texto_extraido
            }), 400
    except Exception as e:
        return jsonify({
            "error": "Erro ao processar o documento.",
            "detalhes": str(e)
        }), 500
