import os
import struct
import io
import time
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)
CORS(app, origins="*", expose_headers=['X-Model-Used'])

# --- LÓGICA DE GERAÇÃO DE ÁUDIO (Inalterada) ---
def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    # ...
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    # ...
    return {"bits_per_sample": bits_per_sample, "rate": rate}

@app.route('/')
def home():
    return "Backend do Gerador de Narração, Chat e Análise está online."

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio_endpoint():
    # ... (endpoint inalterado)

# --- [NOVO] ENDPOINT PARA ANÁLISE DE SENTIMENTO ---
@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment_endpoint():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return jsonify({"error": "Configuração do servidor Gemini incompleta."}), 500
    
    data = request.get_json()
    text_to_analyze = data.get('text')

    if not text_to_analyze:
        return jsonify({"error": "Texto para análise não pode estar vazio."}), 400

    try:
        genai.configure(api_key=gemini_api_key)
        
        # Usando um modelo de texto avançado
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Prompt bem definido para obter uma resposta consistente
        prompt = f"""
        Analise o sentimento do seguinte texto e retorne APENAS UMA das seguintes palavras como resposta: 
        'alegre', 'triste', 'formal', 'zangado', 'neutro', 'inspirador'.

        Texto para analisar: "{text_to_analyze}"
        """
        
        response = model.generate_content(prompt)
        
        # Limpa a resposta para garantir que temos apenas uma palavra
        detected_emotion = response.text.strip().lower().replace('.', '')

        return jsonify({
            "success": True,
            "emotion": detected_emotion
        })

    except Exception as e:
        print(f"Erro na API Gemini (Análise): {e}")
        return jsonify({"error": f"Erro ao analisar o sentimento: {str(e)}"}), 500

# --- LÓGICA DE CHAT COM OPENAI (Inalterada) ---
@app.route('/api/chat', methods=['POST'])
def chat_with_assistant():
    # ... (endpoint inalterado)