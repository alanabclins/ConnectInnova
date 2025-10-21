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
    
    prompt = f"""Você é um avaliador acadêmico especializado em inovação e empreendedorismo.
Analise o projeto abaixo com base nos 15 critérios, usando escala 1-3, lembre-se de que o projeto está resumido:
- 1 (Ruim): Incompleto, sem evidências
- 2 (Médio): Coerente, evidências parciais  
- 3 (Bom): Estruturado, validado

IMPORTANTE: Para cada critério, cite EVIDÊNCIAS ESPECÍFICAS do texto do projeto. Use trechos reais, dados mencionados e informações concretas fornecidas, e classifique com as notas de 1 a 3, escreva pelo menos de 4 a 5 linhas para o feedback de cada um dos campos abaixo.

PROJETO:
Título: {project_data.get('project_title', 'N/A')}
Descrição: {project_data.get('project_description', 'N/A')}
Solução: {project_data.get('solution_proposal', 'N/A')}
Problema: {project_data.get('clarity_problem', 'N/A')}
Inovação: {project_data.get('inovation_grade', 'N/A')}
Impacto: {project_data.get('social_impact', 'N/A')}
Viabilidade: {project_data.get('tec_eco_viability', 'N/A')}
Aplicação: {project_data.get('application_potencial', 'N/A')}

CRITÉRIOS (avalie cada um):
"""

    # Adiciona cada critério de forma compacta
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        prompt += f"{idx}. {criterion['name']}: {criterion['definition']}\n"

    # Adiciona instruções de saída com feedbacks contextualizados
    prompt += """
Responda em JSON (sem markdown):
{
    "full_feedback": "Avaliação geral do projeto em parágrafos. Mencione o nome do projeto, cite dados específicos fornecidos (números, evidências, testes), destaque pontos fortes concretos e sugira melhorias específicas.",
    "criteria_evaluation": {
        "proposta_de_valor": {
            "level": 2,
            "label": "Médio",
            "feedback": "Análise contextualizada: cite trechos específicos do projeto (ex: 'O projeto menciona [dado X] mas não apresenta [evidência Y]'), identifique o que está presente e o que falta."
        },
        "pertinencia_ao_problema": {"level": 2, "label": "Médio", "feedback": "Cite dados/evidências do projeto e avalie adequação da solução.","nota de 1 a 3"},
        "alinhamento_com_objetivos": {"level": 2, "label": "Médio", "feedback": "Cite objetivos mencionados e avalie coerência.","nota de 1 a 3"},
        "adequacao_ao_contexto": {"level": 2, "label": "Médio", "feedback": "Cite público-alvo/contexto mencionado e avalie adaptação.","nota de 1 a 3"},
        "originalidade": {"level": 2, "label": "Médio", "feedback": "Cite elementos inovadores mencionados e avalie grau de novidade.","nota de 1 a 3"},
        "capacidade_de_diferenciacao": {"level": 2, "label": "Médio", "feedback": "Cite diferenciais mencionados e compare com mercado.","nota de 1 a 3"},
        "uso_inteligente_tecnologias": {"level": 2, "label": "Médio", "feedback": "Cite tecnologias mencionadas e avalie escolhas técnicas.","nota de 1 a 3"},
        "impacto_social_ambiental": {"level": 2, "label": "Médio", "feedback": "Cite dados de impacto (números, alcance) e avalie escala.","nota de 1 a 3"},
        "escalabilidade": {"level": 2, "label": "Médio", "feedback": "Avalie potencial de expansão com base no descrito.","nota de 1 a 3"},
        "sustentabilidade": {"level": 2, "label": "Médio", "feedback": "Cite modelo financeiro/parcerias e avalie viabilidade longo prazo.","nota de 1 a 3"},
        "indicadores_de_sucesso": {"level": 2, "label": "Médio", "feedback": "Identifique métricas mencionadas e avalie completude.","nota de 1 a 3"},
        "capacidade_de_melhoria": {"level": 2, "label": "Médio", "feedback": "Avalie se há menção a feedback, iterações ou processos de melhoria.","nota de 1 a 3"},
        "segmento_de_clientes": {"level": 2, "label": "Médio", "feedback": "Cite público-alvo descrito e avalie nível de detalhamento.","nota de 1 a 3"},
        "modelo_geracao_valor": {"level": 2, "label": "Médio", "feedback": "Cite fontes receita/custos mencionados e avalie viabilidade.","nota de 1 a 3"},
        "vantagem_competitiva": {"level": 2, "label": "Médio", "feedback": "Cite vantagens mencionadas e avalie sustentabilidade do diferencial.","nota de 1 a 3"}
    },
    "analysis": {
        "clarity_problem": "Análise agrupada: critérios 1-3, análise de pelo menos 3 a 4 linhas e por fim uma nota geral para o critério de 1 a 3",
        "inovation_grade": "Análise agrupada: critérios 5-7, análise de pelo menos 3 a 4 linhas e por fim uma nota geral para o critério de 1 a 3",
        "social_impact": "Análise agrupada: critérios 8-12, análise de pelo menos 3 a 4 linhas e por fim uma nota geral para o critério de 1 a 3",
        "tec_eco_viability": "Análise agrupada: critério 14, análise de pelo menos 3 a 4 linhas e por fim uma nota geral para o critério de 1 a 3",
        "application_potencial": "Análise agrupada: critérios 4, análise de pelo menos 3 a 4 linhas e por fim uma nota geral para o critério de 1 a 3"
    },
    "resums": {
        "clarity_resum": "Resumo 4-5 frases: proposta, pertinência, análise de pelo menos 3 a 4 linhas com nota de 1 a 3"",
        "inovation_grade_resum": "Resumo 4-5 frases: inovação, diferenciação, tecnologias e nota de 1 a 3"",
        "social_impact_resum": "Resumo 4-5 frases: impacto, sustentabilidade, melhoria e nota de 1 a 3"",
        "tec_eco_viability_resum": "Resumo 4-5 frases: viabilidade, modelo, escalabilidade e nota de 1 a 3"",
        "application_potencial_resum": "Resumo 4-5 frases: aplicação, contexto, clientes e nota de 1 a 3""
    }
}

INSTRUÇÕES DE FEEDBACK:
1. Para CADA critério, cite evidências específicas do projeto (trechos, dados, números)
2. Se algo estiver ausente, mencione explicitamente: "O projeto não menciona..."
3. Se algo estiver presente, cite: "O projeto apresenta X, Y, Z..."
4. No full_feedback, use o nome do projeto e cite exemplos concretos
5. Seja específico e evite feedback genérico
6. Dê notas de 1 = 'ruim', 2 = 'médio' = 3 = 'bom' para cada critério na sua avaliação, junto aos pontos fortes e fracos que você colocar.
7. Coloque ao menos 4 a 5 linhas para cada avaliação de cada critério

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

