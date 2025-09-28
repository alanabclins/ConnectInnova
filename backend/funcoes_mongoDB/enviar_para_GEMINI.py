import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
load_dotenv()


# Configuração da API do Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("✅ Modelo Gemini carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo Gemini. Verifique sua API Key: {e}")
    exit()
def enviar_prompt_para_llm(prompt):
    """Envia o prompt para o modelo Gemini e retorna a resposta."""
    print("   [Task 34] Enviando prompt para o Gemini. Aguardando resposta...")
    try:
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2 # Usamos uma temperatura baixa para garantir o JSON
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        print("   [Task 34] ✅ Resposta recebida da IA.")
        # Tenta carregar o texto da resposta como um JSON para validar
        return json.loads(response.text)
    except Exception as e:
        print(f"   [Task 34] ❌ Erro ao comunicar com a IA: {e}")
        return None
    
