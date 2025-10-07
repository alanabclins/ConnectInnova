import google.generativeai as genai
import os
import sys

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = None

try:
    # CORREÇÃO: Usando o nome de modelo válido.
    model = genai.GenerativeModel("gemini-2.0-flash")
    print("✅ Modelo Gemini carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo Gemini. Verifique sua API Key: {e}")
    sys.exit()


def enviar_para_llm(prompt: str):
    """Envia o prompt para o modelo Gemini e retorna a resposta como texto livre."""
    if not model:
        print("❌ Modelo Gemini não foi inicializado.")
        return None

    print("   [Passo 3] Enviando prompt para LLM...")
    try:
        generation_config = genai.types.GenerationConfig(temperature=0.3)
        response = model.generate_content(prompt, generation_config=generation_config)
        print(f"   [Passo 3] ✅ Resposta da LLM sobre {prompt} recebida com sucesso")
        return response.text
    except Exception as e:
        print(f"   [Passo 3] ❌ Erro ao comunicar com a IA: {e}")
        return None

