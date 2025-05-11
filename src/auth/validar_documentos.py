import pytesseract
from PIL import Image
from flask import jsonify, request
from transformers import pipeline

# Inicialize o modelo LLM uma vez (fora da função)
llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

def validar_documento(documento, cpf):
    try:
        #OCR: Abre a imagem e extrai texto
        image = Image.open(documento.stream)
        texto_extraido = pytesseract.image_to_string(image, lang='por')

        #Checagem direta do CPF no texto extraído
        cpf_presente = cpf in texto_extraido

        #Validação com LLM leve
        prompt = (
            f"Considere o seguinte texto extraído de uma imagem de documento:\n\n"
            f"{texto_extraido}\n\n"
            f"O texto parece conter um CPF válido como '{cpf}' e fazer parte de um documento oficial?"
            f" Responda apenas com 'sim' ou 'não' e justifique brevemente."
        )

        resposta_llm = llm_pipeline(prompt, max_new_tokens=100)[0]['generated_text']

        # 4. Estrutura da resposta
        return jsonify({
            "cpf_encontrado_literalmente": cpf_presente,
            "validacao_llm": resposta_llm,
            "texto_extraido": texto_extraido
        }), 200 if cpf_presente else 400

    except Exception as e:
        return jsonify({
            "error": "Erro ao processar o documento.",
            "detalhes": str(e)
        }), 500
