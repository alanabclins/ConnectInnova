"""
Script de teste para avaliar projetos usando o novo prompt com Gemini
======================================================================

Este script permite testar o novo prompt de avaliação sem precisar
iniciar toda a aplicação ou banco de dados.

Uso:
    python test_gemini_analysis.py
"""

import asyncio
import json

from google import genai

from app.config.config import settings
from app.evaluation_criteria import EVALUATION_CRITERIA

# Dados de projeto de exemplo para teste
EXAMPLE_PROJECT = {
    "project_title": "EcoConnect - Plataforma de Reciclagem Inteligente",
    "project_description": (
        "Aplicativo mobile que conecta pessoas que desejam descartar materiais "
        "recicláveis com cooperativas de reciclagem locais, facilitando a logística "
        "e aumentando a taxa de reciclagem urbana através de gamificação e "
        "otimização de rotas."
    ),
    "solution_proposal": (
        "Plataforma digital com geolocalização que permite agendamento de coletas, "
        "gamificação para incentivar usuários com pontos e recompensas reais, e "
        "dashboard para cooperativas gerenciarem rotas de coleta de forma otimizada "
        "usando algoritmos de otimização."
    ),
    "clarity_problem": (
        "Apenas 4% do lixo reciclável no Brasil é efetivamente reciclado. "
        "Entrevistamos 50 moradores e identificamos que a principal barreira "
        "é a dificuldade de encontrar pontos de coleta e a falta de incentivos. "
        "67% dos entrevistados disseram que reciclariam mais se fosse mais fácil."
    ),
    "inovation_grade": (
        "Utilizamos algoritmos de otimização de rotas baseados em IA e gamificação "
        "com recompensas reais em estabelecimentos parceiros. Não existe solução "
        "similar no mercado brasileiro que integre estes elementos de forma completa. "
        "Temos protótipo funcional em React Native."
    ),
    "social_impact": (
        "Projeto pode beneficiar mais de 10.000 famílias em comunidades onde "
        "cooperativas atuam, gerando renda através da reciclagem e reduzindo "
        "poluição ambiental. Redução estimada de 500 toneladas de lixo não reciclado "
        "por ano na fase piloto."
    ),
    "tec_eco_viability": (
        "App desenvolvido em React Native, backend em Node.js com MongoDB. "
        "Modelo freemium com assinatura premium para empresas que querem métricas "
        "de ESG. Custo inicial de R$50k para MVP. Receita projetada de R$200k no "
        "primeiro ano através de parcerias e assinaturas."
    ),
    "application_potencial": (
        "Piloto validado em 2 bairros com 500 usuários ativos. Taxa de engajamento "
        "de 65% após 3 meses e feedback positivo de 90% dos usuários. Expansão "
        "planejada para 5 cidades em 12 meses. Já temos 3 cooperativas interessadas "
        "em participar."
    )
}


def build_test_prompt(project_data: dict) -> str:
    """
    Constrói o prompt de teste usando a mesma lógica do analysis.py
    """
    # Constrói a tabela de critérios de forma compacta
    criteria_table = ""
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        criteria_table += f"\n{idx}. **{criterion['name']}**: {criterion['definition']}\n"
        # Apenas os níveis extremos e médio para economizar tokens
        for level_data in [criterion['levels'][0], criterion['levels'][2], criterion['levels'][4]]:
            criteria_table += f"N{level_data['level']} ({level_data['label']}): {level_data['description']}\n"

    prompt = f"""
Você é um avaliador acadêmico especializado em inovação e empreendedorismo. Avalie o projeto com base nos critérios abaixo, usando escala 1-5:
- Níveis 1-2 (Ruim): Incompleto, sem evidências
- Nível 3 (Médio): Coerente, evidências parciais
- Nível 4 (Bom): Estruturado, com evidências
- Nível 5 (Excelente): Completo, validado, comprovado

PROJETO:
Título: {project_data['project_title']}
Descrição: {project_data['project_description']}
Solução: {project_data['solution_proposal']}
Problema: {project_data['clarity_problem']}
Inovação: {project_data['inovation_grade']}
Impacto: {project_data['social_impact']}
Viabilidade: {project_data['tec_eco_viability']}
Aplicação: {project_data['application_potencial']}

CRITÉRIOS (analise cada um considerando os níveis):
{criteria_table}

Responda em JSON (sem markdown):
{{
    "full_feedback": "Avaliação geral em 3-4 parágrafos com pontos fortes e áreas de melhoria baseada nos 15 critérios.",
    "analysis": {{
        "clarity_problem": "Análise sobre clareza do problema, pertinência, alinhamento. Cite evidências e indique nível implicitamente.",
        "inovation_grade": "Análise sobre inovação, originalidade, diferenciação, tecnologias. Cite evidências.",
        "social_impact": "Análise sobre impacto social/ambiental, sustentabilidade, melhoria. Cite evidências.",
        "tec_eco_viability": "Análise sobre viabilidade técnica/econômica, modelo de valor, escalabilidade. Cite evidências.",
        "application_potencial": "Análise sobre aplicação, contexto, clientes, indicadores. Cite evidências."
    }},
    "resums": {{
        "clarity_resum": "Resumo em 2-3 frases: problema, pertinência, alinhamento.",
        "inovation_grade_resum": "Resumo em 2-3 frases: inovação, diferenciação, tecnologias.",
        "social_impact_resum": "Resumo em 2-3 frases: impacto, sustentabilidade, melhoria.",
        "tec_eco_viability_resum": "Resumo em 2-3 frases: viabilidade, modelo, escalabilidade.",
        "application_potencial_resum": "Resumo em 2-3 frases: aplicação, contexto, indicadores."
    }}
}}

Avalie com base nas evidências do texto, considere todos os 15 critérios agrupados nos 5 campos acima.
    """

    return prompt


async def test_gemini_analysis():
    """
    Testa o prompt com o Gemini usando dados de exemplo
    """
    print("=" * 80)
    print("TESTE DE AVALIAÇÃO COM GEMINI")
    print("=" * 80)
    print()

    # Verifica se a API key está configurada
    if not settings.GEMINI_API_KEY:
        print("❌ ERRO: Variável de ambiente GEMINI_API_KEY não configurada!")
        print("Configure com: export GEMINI_API_KEY='sua-chave-aqui'")
        return

    print("✅ API Key do Gemini encontrada")
    print()

    # Inicializa cliente
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Constrói o prompt
    print("📝 Construindo prompt com 15 critérios...")
    prompt = build_test_prompt(EXAMPLE_PROJECT)

    print(f"📏 Tamanho do prompt: {len(prompt)} caracteres")
    print()

    # Salva o prompt para visualização
    with open("prompt_generated.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print("💾 Prompt salvo em: prompt_generated.txt")
    print()

    # Envia para o Gemini
    print("🚀 Enviando para o Gemini (modelo: gemini-2.0-flash)...")
    print("⏳ Aguarde... (isso pode levar alguns segundos)")
    print()

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # Captura resposta
        ai_raw = getattr(response, "text", None)

        if not ai_raw or ai_raw.strip() == "":
            print("❌ ERRO: Gemini não retornou nenhum texto.")
            return

        print("✅ Resposta recebida do Gemini!")
        print()

        # Limpa a resposta
        cleaned_response = (
            ai_raw.strip()
            .removeprefix("```json")
            .removeprefix("```JSON")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

        # Tenta parsear JSON
        try:
            ai_data = json.loads(cleaned_response)
            print("✅ JSON válido!")
            print()

            # Salva resposta completa
            with open("gemini_response.json", "w", encoding="utf-8") as f:
                json.dump(ai_data, f, indent=2, ensure_ascii=False)
            print("💾 Resposta completa salva em: gemini_response.json")
            print()

            # Exibe resumo
            print("=" * 80)
            print("RESUMO DA AVALIAÇÃO")
            print("=" * 80)
            print()

            print("📊 FEEDBACK GERAL:")
            print(ai_data.get("full_feedback", "N/A"))
            print()

            if "analysis" in ai_data:
                print("-" * 80)
                print("📋 ANÁLISES DETALHADAS:")
                print("-" * 80)
                for key, value in ai_data["analysis"].items():
                    print(f"\n🔹 {key.upper()}:")
                    print(f"   {value[:200]}..." if len(value) > 200 else f"   {value}")

            if "resums" in ai_data:
                print()
                print("-" * 80)
                print("📝 RESUMOS EXECUTIVOS:")
                print("-" * 80)
                for key, value in ai_data["resums"].items():
                    print(f"\n🔸 {key.upper()}:")
                    print(f"   {value}")

            print()
            print("=" * 80)
            print("✅ TESTE CONCLUÍDO COM SUCESSO!")
            print("=" * 80)

        except json.JSONDecodeError as e:
            print(f"❌ ERRO ao parsear JSON: {e}")
            print()
            print("Resposta recebida (primeiros 500 caracteres):")
            print(cleaned_response[:500])
            print()

            # Salva resposta bruta
            with open("gemini_response_raw.txt", "w", encoding="utf-8") as f:
                f.write(cleaned_response)
            print("💾 Resposta bruta salva em: gemini_response_raw.txt")

    except Exception as e:
        print(f"❌ ERRO ao chamar Gemini: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    Função principal
    """
    print()
    print("🧪 SCRIPT DE TESTE - AVALIAÇÃO DE PROJETOS COM GEMINI")
    print()
    print("Projeto de exemplo: EcoConnect - Plataforma de Reciclagem Inteligente")
    print()

    # Executa teste assíncrono
    asyncio.run(test_gemini_analysis())

    print()
    print("💡 DICA: Para testar com seus próprios dados, edite o dicionário")
    print("   EXAMPLE_PROJECT no início deste arquivo.")
    print()


if __name__ == "__main__":
    main()

