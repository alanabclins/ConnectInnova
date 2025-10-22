"""
TEMPLATE DE PROMPT PARA AVALIAÇÃO DE PROJETOS COM LLM
======================================================

Este módulo contém o template estruturado de prompt que será enviado à LLM
para avaliação de projetos universitários/startups baseado nos 15 critérios
de avaliação documentados em evaluation_criteria.py.

O template inclui:
- Definição do papel do modelo (avaliador acadêmico especializado)
- Instruções fixas de procedimento
- Tabelas de referência para cada critério (níveis 1-5 + indicadores)
- Instruções de formato de saída (JSON estruturado)
"""

from typing import Any, Dict

from app.evaluation_criteria import EVALUATION_CRITERIA


def build_evaluation_prompt(project_data: Dict[str, Any]) -> str:
    """
    Constrói o prompt completo de avaliação baseado nos dados do projeto (otimizado para ~3000 tokens).
    """

    prompt = f"""Você é um avaliador acadêmico sênior, especializado em inovação e empreendedorismo (Lean Canvas).
Sua tarefa é analisar o projeto abaixo e fornecer um feedback detalhado para CADA UM dos 15 critérios de avaliação, além de um feedback geral.

REGRAS DE AVALIAÇÃO:
- Use a escala 1-3: 1 (Ruim: Incompleto, sem evidências), 2 (Médio: Coerente, evidências parciais), 3 (Bom: Estruturado, validado).
- Para CADA critério, escreva um feedback de 4-5 linhas.
- CRÍTICO: Seu feedback deve citar EVIDÊNCIAS ESPECÍFICAS do texto do projeto. Use trechos reais, dados e informações concretas.
- Se algo estiver ausente, mencione explicitamente: "O projeto não apresenta dados sobre..."
- Se algo estiver presente, cite: "O projeto cita que '...' o que demonstra..."

PROJETO A SER AVALIADO:
- Título: {project_data.get('project_title', 'N/A')}
- Descrição: {project_data.get('project_description', 'N/A')}
- Solução: {project_data.get('solution_proposal', 'N/A')}
- Problema: {project_data.get('clarity_problem', 'N/A')}
- Inovação: {project_data.get('inovation_grade', 'N/A')}
- Impacto: {project_data.get('social_impact', 'N/A')}
- Viabilidade: {project_data.get('tec_eco_viability', 'N/A')}
- Aplicação: {project_data.get('application_potencial', 'N/A')}

LISTA DE CRITÉRIOS OBRIGATÓRIOS (Avalie todos os 15):
1. proposta_de_valor: {EVALUATION_CRITERIA['proposta_de_valor']['definition']}
2. pertinencia_ao_problema: {EVALUATION_CRITERIA['pertinencia_ao_problema']['definition']}
3. alinhamento_com_objetivos: {EVALUATION_CRITERIA['alinhamento_com_objetivos']['definition']}
4. adequacao_ao_contexto: {EVALUATION_CRITERIA['adequacao_ao_contexto']['definition']}
5. originalidade: {EVALUATION_CRITERIA['originalidade']['definition']}
6. capacidade_de_diferenciacao: {EVALUATION_CRITERIA['capacidade_de_diferenciacao']['definition']}
7. uso_inteligente_tecnologias: {EVALUATION_CRITERIA['uso_inteligente_tecnologias']['definition']}
8. impacto_social_ambiental: {EVALUATION_CRITERIA['impacto_social_ambiental']['definition']}
9. escalabilidade: {EVALUATION_CRITERIA['escalabilidade']['definition']}
10. sustentabilidade: {EVALUATION_CRITERIA['sustentabilidade']['definition']}
11. indicadores_de_sucesso: {EVALUATION_CRITERIA['indicadores_de_sucesso']['definition']}
12. capacidade_de_melhoria: {EVALUATION_CRITERIA['capacidade_de_melhoria']['definition']}
13. segmento_de_clientes: {EVALUATION_CRITERIA['segmento_de_clientes']['definition']}
14. modelo_geracao_valor: {EVALUATION_CRITERIA['modelo_geracao_valor']['definition']}
15. vantagem_competitiva: {EVALUATION_CRITERIA['vantagem_competitiva']['definition']}

INSTRUÇÃO DE SAÍDA:
Sua resposta deve ser APENAS um objeto JSON válido, sem markdown (```json) ou qualquer outro texto. Siga exatamente a estrutura abaixo:

{{
  "full_feedback": "Escreva aqui um resumo executivo da análise geral do projeto (4-5 frases), citando o nome do projeto e os principais pontos fortes e fracos.",
  "criteria_evaluation": {{
    "proposta_de_valor": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "pertinencia_ao_problema": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "alinhamento_com_objetivos": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "adequacao_ao_contexto": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "originalidade": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "capacidade_de_diferenciacao": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "uso_inteligente_tecnologias": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "impacto_social_ambiental": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "escalabilidade": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "sustentabilidade": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "indicadores_de_sucesso": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "capacidade_de_melhoria": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "segmento_de_clientes": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "modelo_geracao_valor": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }},
    "vantagem_competitiva": {{
      "level": <int 1, 2 ou 3>,
      "label": "<String Ruim, Médio ou Bom>",
      "feedback": "<Seu feedback de 4-5 linhas citando evidências para este critério...>"
    }}
  }}
}}
"""
    return prompt


def build_simple_prompt(
    project_title: str, project_description: str, solution_proposal: str
) -> str:
    """
    Constrói uma versão simplificada do prompt para projetos com dados mínimos.

    Args:
        project_title: Título do projeto
        project_description: Descrição do projeto
        solution_proposal: Proposta de solução

    Returns:
        String contendo o prompt simplificado
    """
    project_data = {
        "project_title": project_title,
        "project_description": project_description,
        "solution_proposal": solution_proposal,
        "clarity_problem": "Não informado",
        "inovation_grade": "Não informado",
        "social_impact": "Não informado",
        "tec_eco_viability": "Não informado",
        "application_potencial": "Não informado",
    }

    return build_evaluation_prompt(project_data)


def build_resum_prompt(project_data: dict[str, Any]) -> str:
    """
    Constrói o prompt para resumo do projeto.
    """
    prompt2 = f"""
Seu papel é resumir os seguintes campos de cada projeto:
PROJETO:
Título: {project_data.get('project_title', 'N/A')}
Descrição: {project_data.get('project_description', 'N/A')}
Solução: {project_data.get('solution_proposal', 'N/A')}
Problema: {project_data.get('clarity_problem', 'N/A')}
Inovação: {project_data.get('inovation_grade', 'N/A')}
Impacto: {project_data.get('social_impact', 'N/A')}
Viabilidade: {project_data.get('tec_eco_viability', 'N/A')}
Aplicação: {project_data.get('application_potencial', 'N/A')}

IMPORTANTE! VOCÊ DEVE RETORNAR UM RESUMO PARA CADA CAMPO SEPARADO, EM FORMATO JSON SEM MARKDOWN no seguinte formato:
{{
    "resums": {{
        "clarity_resum": "...",
        "inovation_grade_resum": "...",
        "social_impact_resum": "...",
        "tec_eco_viability_resum": "...",
        "application_potencial_resum": "..."
    }}
}}
"""
    return prompt2


def get_criteria_summary() -> str:
    """
    Retorna um resumo dos critérios de avaliação para documentação.

    Returns:
        String formatada com lista de todos os critérios
    """
    summary = "CRITÉRIOS DE AVALIAÇÃO:\n\n"
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        summary += f"{idx}. {criterion['name']}\n"
        summary += f"   {criterion['definition']}\n\n"
    return summary


# Template de exemplo para testes
EXAMPLE_PROJECT_DATA = {
    "project_title": "EcoConnect - Plataforma de Reciclagem Inteligente",
    "project_description": (
        "Aplicativo mobile que conecta pessoas que desejam descartar materiais "
        "recicláveis com cooperativas de reciclagem locais, facilitando a logística "
        "e aumentando a taxa de reciclagem urbana."
    ),
    "solution_proposal": (
        "Plataforma digital com geolocalização que permite agendamento de coletas, "
        "gamificação para incentivar usuários, e dashboard para cooperativas "
        "gerenciarem rotas de coleta de forma otimizada."
    ),
    "clarity_problem": (
        "Apenas 4% do lixo reciclável no Brasil é efetivamente reciclado. "
        "Entrevistamos 50 moradores e identificamos que a principal barreira "
        "é a dificuldade de encontrar pontos de coleta e a falta de incentivos."
    ),
    "inovation_grade": (
        "Utilizamos algoritmos de otimização de rotas e gamificação com recompensas "
        "reais em estabelecimentos parceiros. Não existe solução similar no mercado "
        "que integre estes elementos."
    ),
    "social_impact": (
        "Projeto pode beneficiar mais de 10.000 famílias em comunidades onde "
        "cooperativas atuam, gerando renda através da reciclagem e reduzindo "
        "poluição ambiental."
    ),
    "tec_eco_viability": (
        "App desenvolvido em React Native, backend em Node.js. Modelo freemium "
        "com assinatura premium para empresas. Custo inicial de R$50k para MVP."
    ),
    "application_potencial": (
        "Piloto validado em 2 bairros com 500 usuários ativos. Taxa de engajamento "
        "de 65% e feedback positivo de 90% dos usuários. Expansão planejada para "
        "5 cidades em 12 meses."
    ),
}


if __name__ == "__main__":
    # Teste do template
    print("=" * 80)
    print("TEMPLATE DE PROMPT PARA AVALIAÇÃO DE PROJETOS")
    print("=" * 80)
    print()
    print(get_criteria_summary())
    print()
    print("=" * 80)
    print("EXEMPLO DE PROMPT COMPLETO:")
    print("=" * 80)
    print()
    prompt = build_evaluation_prompt(EXAMPLE_PROJECT_DATA)
    print(prompt)
