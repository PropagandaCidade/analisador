import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# Endpoint raiz para verificação de status
@app.route('/')
def home():
    return "Serviço de Análise de Sentimento está online."

# Endpoint principal para análise de sentimento
@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment_endpoint():
    # 1. Pega a chave da API das variáveis de ambiente do Render
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return jsonify({"error": "Configuração do servidor Gemini incompleta."}), 500
    
    # 2. Pega o texto enviado pelo frontend (via PHP)
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "Texto para análise não pode estar vazio."}), 400
    
    text_to_analyze = data.get('text')

    try:
        # 3. Configura e chama a API do Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        prompt = f"""
        Analise o sentimento do seguinte texto e retorne APENAS UMA das seguintes palavras como resposta: 
        'alegre', 'triste', 'formal', 'zangado', 'neutro', 'inspirador'.

        Texto para analisar: "{text_to_analyze}"
        """
        
        response = model.generate_content(prompt)
        
        # 4. Limpa a resposta e a retorna como JSON
        detected_emotion = response.text.strip().lower().replace('.', '')

        return jsonify({
            "success": True,
            "emotion": detected_emotion
        })

    except Exception as e:
        # Loga o erro no console do Render para debug
        print(f"Erro na API Gemini (Análise): {e}")
        return jsonify({"error": f"Erro ao analisar o sentimento: {str(e)}"}), 500

# Esta parte não é estritamente necessária se você usar o Gunicorn, 
# mas é uma boa prática para testes locais.
if __name__ == '__main__':
    app.run()