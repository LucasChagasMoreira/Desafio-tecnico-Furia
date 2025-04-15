import pytesseract
from PIL import Image
from flask import jsonify, request

def validar_documento(documento):
    try:
        
        image = Image.open(documento.stream)
        # Extrai o texto da imagem com pytesseract
        texto_extraido = pytesseract.image_to_string(image, lang='por')
    
        # Retorna o texto extraído no formato JSON
        return jsonify({"texto": texto_extraido}), 200
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro com detalhes
        return jsonify({"error": "Erro ao processar o documento.", "detalhes": str(e)}), 500
