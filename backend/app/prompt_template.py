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
    
    prompt = f"""Avaliador acadêmico especializado em inovação e empreendedorismo. Avalie usando escala 1-5:
1-2=Ruim (incompleto, sem evidências), 3=Médio (coerente, evidências parciais), 4=Bom (estruturado, evidências claras), 5=Excelente (validado, comprovado).

PROJETO:
Título: {project_data.get('project_title', 'N/A')}
Descrição: {project_data.get('project_description', 'N/A')}
Solução: {project_data.get('solution_proposal', 'N/A')}
Problema: {project_data.get('clarity_problem', 'N/A')}
Inovação: {project_data.get('inovation_grade', 'N/A')}
Impacto: {project_data.get('social_impact', 'N/A')}
Viabilidade: {project_data.get('tec_eco_viability', 'N/A')}
Aplicação: {project_data.get('application_potencial', 'N/A')}

CRITÉRIOS (15 critérios baseados em Lean Canvas):
"""

    # Adiciona cada critério de forma compacta
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        # Pega apenas o nível médio (3) como referência
        level_3 = criterion['levels'][2]
        prompt += f"{idx}. {criterion['name']}: {criterion['definition']} N3={level_3['description']}\n"

    # Adiciona instruções de saída - formato compatível com o sistema existente
    prompt += """
Responda em JSON (sem markdown):
{
    "full_feedback": "Avaliação geral em 3-4 parágrafos, pontos fortes e melhorias.",
    "analysis": {
        "clarity_problem": "Análise agrupando critérios 1-3 (Proposta Valor, Pertinência, Alinhamento). Cite evidências.",
        "inovation_grade": "Análise agrupando critérios 4-7 (Originalidade, Diferenciação, Tecnologias, Vantagem). Cite evidências.",
        "social_impact": "Análise agrupando critérios 8-12 (Impacto, Escalabilidade, Sustentabilidade, Indicadores, Melhoria). Cite evidências.",
        "tec_eco_viability": "Análise agrupando critério 14 (Modelo Valor). Cite evidências.",
        "application_potencial": "Análise agrupando critérios 4,13 (Adequação Contexto, Segmento Clientes). Cite evidências."
    },
    "resums": {
        "clarity_resum": "Resumo 2-3 frases: proposta, pertinência, alinhamento.",
        "inovation_grade_resum": "Resumo 2-3 frases: inovação, diferenciação, tecnologia.",
        "social_impact_resum": "Resumo 2-3 frases: impacto, sustentabilidade, melhoria.",
        "tec_eco_viability_resum": "Resumo 2-3 frases: viabilidade, modelo, escalabilidade.",
        "application_potencial_resum": "Resumo 2-3 frases: aplicação, contexto, clientes."
    }
}

Avalie com evidências do texto, considere os 15 critérios agrupados nos 5 campos.
"""

    return prompt


def build_simple_prompt(project_title: str, project_description: str, solution_proposal: str) -> str:
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
        'project_title': project_title,
        'project_description': project_description,
        'solution_proposal': solution_proposal,
        'clarity_problem': 'Não informado',
        'inovation_grade': 'Não informado',
        'social_impact': 'Não informado',
        'tec_eco_viability': 'Não informado',
        'application_potencial': 'Não informado'
    }

    return build_evaluation_prompt(project_data)


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
    'project_title': 'EcoConnect - Plataforma de Reciclagem Inteligente',
    'project_description': (
        'Aplicativo mobile que conecta pessoas que desejam descartar materiais '
        'recicláveis com cooperativas de reciclagem locais, facilitando a logística '
        'e aumentando a taxa de reciclagem urbana.'
    ),
    'solution_proposal': (
        'Plataforma digital com geolocalização que permite agendamento de coletas, '
        'gamificação para incentivar usuários, e dashboard para cooperativas '
        'gerenciarem rotas de coleta de forma otimizada.'
    ),
    'clarity_problem': (
        'Apenas 4% do lixo reciclável no Brasil é efetivamente reciclado. '
        'Entrevistamos 50 moradores e identificamos que a principal barreira '
        'é a dificuldade de encontrar pontos de coleta e a falta de incentivos.'
    ),
    'inovation_grade': (
        'Utilizamos algoritmos de otimização de rotas e gamificação com recompensas '
        'reais em estabelecimentos parceiros. Não existe solução similar no mercado '
        'que integre estes elementos.'
    ),
    'social_impact': (
        'Projeto pode beneficiar mais de 10.000 famílias em comunidades onde '
        'cooperativas atuam, gerando renda através da reciclagem e reduzindo '
        'poluição ambiental.'
    ),
    'tec_eco_viability': (
        'App desenvolvido em React Native, backend em Node.js. Modelo freemium '
        'com assinatura premium para empresas. Custo inicial de R$50k para MVP.'
    ),
    'application_potencial': (
        'Piloto validado em 2 bairros com 500 usuários ativos. Taxa de engajamento '
        'de 65% e feedback positivo de 90% dos usuários. Expansão planejada para '
        '5 cidades em 12 meses.'
    )
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

