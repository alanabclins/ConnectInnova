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
    Constrói o prompt completo de avaliação baseado nos dados do projeto.
    
    Args:
        project_data: Dicionário com dados do projeto incluindo:
            - project_title: Título do projeto
            - project_description: Descrição do projeto
            - solution_proposal: Proposta de solução
            - clarity_problem: Informações sobre o problema
            - inovation_grade: Informações sobre inovação
            - social_impact: Informações sobre impacto social
            - tec_eco_viability: Informações sobre viabilidade
            - application_potencial: Informações sobre potencial de aplicação
            
    Returns:
        String contendo o prompt completo formatado
    """

    prompt = f"""
# PAPEL E CONTEXTO

Você é um **avaliador acadêmico especializado em inovação, empreendedorismo e projetos tecnológicos**. 
Seu objetivo é avaliar projetos universitários e startups de forma rigorosa, objetiva e construtiva, 
utilizando critérios bem definidos baseados em metodologias como Lean Canvas, Business Model Canvas 
e frameworks de avaliação de inovação.

Você possui expertise em:
- Análise de modelos de negócio e geração de valor
- Avaliação de inovação tecnológica e social
- Validação de problemas e soluções
- Mensuração de impacto e escalabilidade
- Empreendedorismo e gestão de startups

---

# INSTRUÇÕES GERAIS DE PROCEDIMENTO

1. **Avalie cada critério SEPARADAMENTE e INDEPENDENTEMENTE**
2. **Compare o texto do projeto com as definições de níveis apresentadas**
3. **Justifique cada avaliação com base em EVIDÊNCIAS TEXTUAIS** encontradas no projeto
4. **Seja objetivo, construtivo e específico** nos feedbacks
5. **Identifique lacunas e oportunidades de melhoria** de forma clara
6. **Utilize a escala de 1 a 5** conforme as definições detalhadas abaixo
7. **Forneça next_steps acionáveis** que ajudem o time a evoluir para o próximo nível

---

# ESCALA DE CLASSIFICAÇÃO

- **RUIM (Níveis 1-2)**: Resposta incompleta, incoerente, genérica ou sem fundamentação. Ausência de evidências ou validação.
- **MÉDIO (Nível 3)**: Resposta coerente, mas com falhas significativas de clareza, validação ou aplicabilidade. Evidências parciais.
- **BOM (Nível 4)**: Resposta bem estruturada, com evidências claras, aplicabilidade demonstrada e boa fundamentação.
- **EXCELENTE (Nível 5)**: Resposta completa, validada com evidências sólidas, impacto comprovado e qualidade exemplar.

---

# DADOS DO PROJETO A SER AVALIADO

**Título do Projeto:**
{project_data.get('project_title', 'Não informado')}

**Descrição do Projeto:**
{project_data.get('project_description', 'Não informado')}

**Proposta de Solução:**
{project_data.get('solution_proposal', 'Não informado')}

**Informações sobre o Problema:**
{project_data.get('clarity_problem', 'Não informado')}

**Informações sobre Inovação:**
{project_data.get('inovation_grade', 'Não informado')}

**Informações sobre Impacto Social:**
{project_data.get('social_impact', 'Não informado')}

**Informações sobre Viabilidade Técnica e Econômica:**
{project_data.get('tec_eco_viability', 'Não informado')}

**Informações sobre Potencial de Aplicação:**
{project_data.get('application_potencial', 'Não informado')}

---

# TABELA DE REFERÊNCIA: CRITÉRIOS DE AVALIAÇÃO

Avalie o projeto nos seguintes 15 critérios, utilizando as definições e escalas detalhadas abaixo:

"""

    # Adiciona cada critério com suas definições e níveis
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        prompt += f"""
## {idx}. {criterion['name']}

**Definição:** {criterion['definition']}

**Indicadores Mensuráveis a Buscar:**
{chr(10).join(f'- {indicator}' for indicator in criterion['measurable_indicators'])}

**Escala de Níveis:**

"""
        # Adiciona cada nível do critério
        for level_data in criterion['levels']:
            prompt += f"""**Nível {level_data['level']} ({level_data['label']}):**
- Descrição: {level_data['description']}
- Sinais textuais esperados:
{chr(10).join(f'  • {indicator}' for indicator in level_data['indicators'])}

"""

    # Adiciona instruções de saída
    prompt += """
---

# FORMATO DE SAÍDA OBRIGATÓRIO

Você DEVE responder EXCLUSIVAMENTE em formato JSON válido, seguindo EXATAMENTE a estrutura abaixo.
NÃO inclua comentários, explicações fora do JSON ou blocos de código markdown.

```json
{
    "full_feedback": "Avaliação geral do projeto em 3-5 parágrafos, destacando principais pontos fortes e áreas de melhoria de forma construtiva e específica.",
    
    "criteria_evaluation": {
        "proposta_de_valor": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto, explicando por que este nível foi atribuído.",
            "next_step": "Ação concreta e acionável para evoluir para o próximo nível."
        },
        "pertinencia_ao_problema": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "alinhamento_com_objetivos": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "adequacao_ao_contexto": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "originalidade": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "capacidade_de_diferenciacao": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "uso_inteligente_tecnologias": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "impacto_social_ambiental": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "escalabilidade": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "sustentabilidade": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "indicadores_de_sucesso": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "capacidade_de_melhoria": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "segmento_de_clientes": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "modelo_geracao_valor": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        },
        "vantagem_competitiva": {
            "level": 1,
            "label": "Ruim",
            "feedback": "Descrição objetiva e específica baseada em evidências do texto.",
            "next_step": "Ação concreta para melhorar."
        }
    },
    
    "summary": {
        "average_score": 0.0,
        "strengths": [
            "Ponto forte 1 com base em evidências",
            "Ponto forte 2 com base em evidências",
            "Ponto forte 3 com base em evidências"
        ],
        "improvement_areas": [
            "Área de melhoria 1 específica",
            "Área de melhoria 2 específica",
            "Área de melhoria 3 específica"
        ],
        "priority_actions": [
            "Ação prioritária 1 para maior impacto",
            "Ação prioritária 2 para maior impacto",
            "Ação prioritária 3 para maior impacto"
        ]
    }
}
```

---

# DIRETRIZES FINAIS

1. **Baseie-se APENAS nas informações fornecidas no projeto**
2. **Cite evidências específicas** do texto ao justificar cada nível
3. **Seja construtivo e educativo** nos feedbacks
4. **Forneça next_steps práticos e acionáveis**
5. **Mantenha objetividade e imparcialidade**
6. **Use linguagem clara e profissional**
7. **Calcule average_score como a média aritmética dos 15 níveis**
8. **Identifique 3-5 pontos fortes reais baseados em evidências**
9. **Identifique 3-5 áreas de melhoria prioritárias**
10. **Sugira 3-5 ações prioritárias ordenadas por impacto**

---

Agora, proceda com a avaliação completa do projeto apresentado, seguindo rigorosamente todas as instruções e o formato JSON especificado.
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

