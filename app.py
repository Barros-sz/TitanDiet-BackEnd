import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import DIETA_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODELO_GEMINI = "gemini-2.5-flash"

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": ["https://titan-diet-front-end.vercel.app"],
    "methods": ["POST", "GET", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

def generate_diet(objetivo, dia_livre, detalhes):
    conteudo_prompt = f"Objetivo: {objetivo}\nDia livre desejado: {dia_livre}\nDetalhes do cliente: {detalhes}"
    
    response = client.models.generate_content(
        model=MODELO_GEMINI,
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=DIETA_SCHEMA,
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Nutricionista Barros online e pronta para os frangos!",
        "version": "1.0"
    }), 200

@app.route("/gerar-dieta", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data or "objetivo" not in data:
        return jsonify({
            "status": "error",
            "message": "É necessário informar ao menos o 'objetivo' no JSON."
        }), 400
        
    objetivo = data.get("objetivo")
    dia_livre = data.get("dia_livre", "Não especificado")
    detalhes = data.get("detalhes", "Nenhum detalhe adicional")
    
    if len(objetivo.strip()) < 3:
        return jsonify({
            "status": "error",
            "message": "O objetivo está muito curto ou inválido."
        }), 400
    
    try:
        dieta_json_string = generate_diet(objetivo, dia_livre, detalhes)
        dieta_estruturada = json.loads(dieta_json_string)
        
        return jsonify({
            "status": "success",
            "dados_cliente": {
                "objetivo": objetivo,
                "dia_livre": dia_livre,
                "detalhes": detalhes
            },
            "dieta": dieta_estruturada
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro na geração da dieta: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)