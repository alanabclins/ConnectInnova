import google.generativeai as genai
import json
import os
import sys

import google.generativeai as genai
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
    sys.exit()
def enviar_para_llm(prompt: str):
    """Envia o prompt para o modelo Gemini e retorna a resposta como texto livre."""
    print("   [Task 34] Enviando prompt para o Gemini. Aguardando resposta...")
    try:
        generation_config = genai.types.GenerationConfig(
            temperature=0.3  # Temperatura moderada para análise criativa mas consistente
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        print("   [Task 34] ✅ Resposta recebida da IA.")
        # Retorna o texto da resposta diretamente, sem tentar fazer parse de JSON
        return response.text
    except Exception as e:
        print(f"   [Task 34] ❌ Erro ao comunicar com a IA: {e}")
        return None

# Função de compatibilidade (deprecated)
def enviar_prompt_para_llm(prompt):
    """DEPRECATED: Use enviar_para_llm() em vez desta função."""
    return enviar_para_llm(prompt)

