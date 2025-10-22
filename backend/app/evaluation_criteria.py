"""
TABELA DE NÍVEIS POR CRITÉRIO DE AVALIAÇÃO (Escala 1-3)
========================================================

Critérios de avaliação com escala simplificada de 3 níveis.

Classificação de Níveis (Escala 1-3):
- RUIM (Nível 1): Resposta incompleta, incoerente, genérica ou sem base
- MÉDIO (Nível 2): Coerente, mas com falhas de clareza, validação ou aplicabilidade
- BOM (Nível 3): Bem estruturado, com evidências claras e aplicabilidade demonstrada
"""

from typing import Dict, List, TypedDict


class CriterionLevel(TypedDict):
    level: int
    label: str
    description: str
    indicators: List[str]


class EvaluationCriterion(TypedDict):
    name: str
    definition: str
    levels: List[CriterionLevel]
    measurable_indicators: List[str]


EVALUATION_CRITERIA: Dict[str, EvaluationCriterion] = {
    "proposta_de_valor": {
        "name": "Proposta de Valor",
        "definition": "Clareza sobre o benefício central e diferencial da solução.",
        "measurable_indicators": [
            "Problema validado",
            "Valor claro",
            "Feedback usuários",
            "Diferencial competitivo",
            "Protótipo/MVP",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não apresenta claramente problema nem diferencial.",
                "indicators": ["Sem descrição problema", "Sem benefícios", "Genérico"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Problema e solução apresentados, diferenciação pouco evidente.",
                "indicators": [
                    "Problema sem validação",
                    "Solução básica",
                    "Diferencial não fundamentado",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Problema e solução sólidos, diferencial validado com evidências.",
                "indicators": [
                    "Problema validado",
                    "Solução detalhada",
                    "Diferencial comprovado",
                    "Feedback positivo",
                ],
            },
        ],
    },
    "pertinencia_ao_problema": {
        "name": "Pertinência ao Problema",
        "definition": "Grau em que a solução responde efetivamente à necessidade.",
        "measurable_indicators": [
            "Validação do problema",
            "Entrevistas usuários",
            "Dados relevância",
            "Testes/protótipos",
            "Feedback stakeholders",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Solução não relacionada ao problema.",
                "indicators": [
                    "Desconectada",
                    "Sem relação lógica",
                    "Não aborda necessidade",
                ],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Aborda problema de forma limitada ou superficial.",
                "indicators": [
                    "Parcialmente adequada",
                    "Resolve parte",
                    "Falta profundidade",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Resolve problema de forma consistente, comprovada com dados/feedback.",
                "indicators": ["Validada", "Dados efetividade", "Feedback positivo"],
            },
        ],
    },
    "alinhamento_com_objetivos": {
        "name": "Alinhamento com Objetivos",
        "definition": "Coerência entre solução e objetivos do projeto.",
        "measurable_indicators": [
            "Metas documentadas",
            "Coerência entregas-objetivos",
            "Métricas contribuição",
            "Análise resultados",
            "Rastreabilidade",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não alinhada aos objetivos.",
                "indicators": ["Objetivos ausentes", "Sem relação metas", "Desconexão"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Atende parcialmente objetivos, sem detalhar como.",
                "indicators": ["Objetivos vagos", "Alinhamento incompleto", "Falta clareza"],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Alinhamento completo com evidências de contribuição aos objetivos.",
                "indicators": [
                    "Objetivos mensuráveis",
                    "Métricas comprovam",
                    "Resultados demonstrados",
                ],
            },
        ],
    },
    "adequacao_ao_contexto": {
        "name": "Adequação ao Contexto",
        "definition": "Adaptação às condições, público-alvo e restrições.",
        "measurable_indicators": [
            "Perfil público",
            "Testes usabilidade",
            "Feedback contextualizado",
            "Adaptações documentadas",
            "Análise restrições",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não considera contexto nem público-alvo.",
                "indicators": ["Sem público", "Contexto ignorado", "Genérica"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Considera público e ambiente, pouca adaptação prática.",
                "indicators": [
                    "Público sem detalhes",
                    "Contexto mencionado",
                    "Adaptações mínimas",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Totalmente adaptada, validada em campo com feedback contextualizado.",
                "indicators": ["Personas validadas", "Testes reais", "Adaptações efetivas"],
            },
        ],
    },
    "originalidade": {
        "name": "Originalidade",
        "definition": "Grau de inovação ou aprimoramento da solução.",
        "measurable_indicators": [
            "Comparação com existentes",
            "Tecnologias/abordagens inéditas",
            "Reconhecimento inovação",
            "Diferenciação técnica",
            "Feedback sobre inovação",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Cópia ou pequenas variações.",
                "indicators": ["Reprodução conhecida", "Sem novidade", "Baixa diferenciação"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Introduz elementos novos, sem grande diferenciação.",
                "indicators": [
                    "Elementos inovadores",
                    "Combinação ideias",
                    "Inovação incremental",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Solução criativa e disruptiva, reconhecida pela originalidade.",
                "indicators": [
                    "Inovação radical",
                    "Reconhecimento",
                    "Originalidade comprovada",
                ],
            },
        ],
    },
    "capacidade_de_diferenciacao": {
        "name": "Capacidade de Diferenciação",
        "definition": "Grau de destaque frente a alternativas existentes.",
        "measurable_indicators": [
            "Benchmarking",
            "Percepção valor usuários",
            "Desempenho superior",
            "Diferenciais técnicos",
            "Feedback comparativo",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum ou poucos diferenciais.",
                "indicators": ["Sem distinção", "Diferenciais vagos", "Irrelevantes"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Diferenciais moderados em alguns aspectos.",
                "indicators": [
                    "Alguns diferenciais",
                    "Distinção parcial",
                    "Relevância moderada",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Diferenciais sólidos com evidências e percepção positiva.",
                "indicators": [
                    "Comprovados com dados",
                    "Percepção validada",
                    "Superioridade demonstrada",
                ],
            },
        ],
    },
    "uso_inteligente_tecnologias": {
        "name": "Uso Inteligente de Tecnologias",
        "definition": "Integração estratégica de tecnologias para potencializar a solução.",
        "measurable_indicators": [
            "Justificativa técnica",
            "Frameworks/ferramentas",
            "Protótipos funcionais",
            "Eficiência técnica",
            "Trade-offs",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Uso inadequado, inexistente ou básico sem justificativa.",
                "indicators": ["Não mencionadas", "Inadequadas", "Sem justificativa"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Uso adequado, pouca otimização.",
                "indicators": ["Apropriadas", "Justificativa básica", "Sem otimização"],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Integra de forma inovadora, estratégica e comprovadamente eficaz.",
                "indicators": ["Bem fundamentadas", "Uso otimizado", "Eficácia comprovada"],
            },
        ],
    },
    "impacto_social_ambiental": {
        "name": "Impacto Social ou Ambiental",
        "definition": "Benefício concreto para pessoas, comunidades ou meio ambiente.",
        "measurable_indicators": [
            "Dados quantitativos",
            "Resultados qualitativos",
            "Alcance beneficiários",
            "Feedback comunidades",
            "Métricas ESG/ODS",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum impacto identificável ou apenas potencial sem evidência.",
                "indicators": ["Não menciona", "Sem evidências", "Genérico"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Impacto perceptível em pequena escala.",
                "indicators": [
                    "Benefícios documentados",
                    "Impacto localizado",
                    "Evidências iniciais",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Impacto significativo mensurado com evidências concretas.",
                "indicators": ["Quantificado", "Grande alcance", "Reconhecimento externo"],
            },
        ],
    },
    "escalabilidade": {
        "name": "Escalabilidade",
        "definition": "Potencial de ampliação ou replicação em outros contextos.",
        "measurable_indicators": [
            "Modelo replicável",
            "Documentação processos",
            "Testes múltiplos contextos",
            "Requisitos expansão",
            "Casos replicação",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não replicável ou sem estrutura.",
                "indicators": ["Não transferível", "Sem documentação", "Muitas barreiras"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Escalável com adaptações significativas.",
                "indicators": [
                    "Replicável com ajustes",
                    "Documentação parcial",
                    "Escalabilidade limitada",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Altamente escalável, validada em novos contextos.",
                "indicators": [
                    "Replicação comprovada",
                    "Documentação completa",
                    "Múltiplos contextos",
                ],
            },
        ],
    },
    "sustentabilidade": {
        "name": "Sustentabilidade",
        "definition": "Capacidade de manter resultados e operações no longo prazo.",
        "measurable_indicators": [
            "Plano financeiro",
            "Parcerias estratégicas",
            "Engajamento stakeholders",
            "Viabilidade financeira",
            "Estratégias continuidade",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não se mantém ou apenas curto prazo.",
                "indicators": ["Dependência externa", "Sem plano", "Inviável longo prazo"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Estratégias parciais de continuidade.",
                "indicators": [
                    "Planejamento parcial",
                    "Recursos incertos",
                    "Sustentabilidade questionável",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Sustentabilidade comprovada com planos e parceiros consolidados.",
                "indicators": [
                    "Modelo validado",
                    "Parcerias estabelecidas",
                    "Autossustentável",
                ],
            },
        ],
    },
    "indicadores_de_sucesso": {
        "name": "Indicadores de Sucesso",
        "definition": "Métricas e instrumentos para mensurar resultados e impactos.",
        "measurable_indicators": [
            "KPIs definidos",
            "Métricas quantificáveis",
            "Relatórios periódicos",
            "Monitoramento contínuo",
            "Dashboards",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhuma métrica ou métricas genéricas não aplicadas.",
                "indicators": ["Sem métricas", "Vagas", "Não coletadas"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Métricas definidas, sem mensuração completa.",
                "indicators": [
                    "KPIs identificados",
                    "Coleta parcial",
                    "Mensuração incompleta",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Métricas aplicadas e analisadas com resultados documentados.",
                "indicators": [
                    "Sistema completo",
                    "Coleta contínua",
                    "Análises regulares",
                    "Resultados documentados",
                ],
            },
        ],
    },
    "capacidade_de_melhoria": {
        "name": "Capacidade de Melhoria",
        "definition": "Grau de aprendizado, ajustes e evolução contínua permitidos.",
        "measurable_indicators": [
            "Uso feedback",
            "Histórico iterações",
            "Planos melhoria",
            "Documentação mudanças",
            "Processos ágeis",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não permite ajustes ou recebe feedback mas não aplica.",
                "indicators": ["Rígida", "Feedback ignorado", "Sem processo"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Melhora pontualmente sem processo estruturado.",
                "indicators": ["Melhorias ad-hoc", "Sem sistematização", "Processo básico"],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Cultura contínua de melhoria com base em dados e feedback.",
                "indicators": [
                    "Processo definido",
                    "Dados direcionam",
                    "Histórico iterações",
                    "Metodologia ágil",
                ],
            },
        ],
    },
    "segmento_de_clientes": {
        "name": "Segmento de Clientes",
        "definition": "Clareza na definição do público-alvo da solução.",
        "measurable_indicators": [
            "Personas",
            "Dados segmentação",
            "Validação público",
            "Testes usabilidade",
            "Pesquisas mercado",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Público não definido ou genérico sem dados.",
                "indicators": ["Ausente", "Sem dados", "Vago"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Público identificado, sem validação.",
                "indicators": ["Identificado", "Descrição básica", "Sem validação"],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Segmentos validados com personas e comportamentos detalhados.",
                "indicators": [
                    "Personas validadas",
                    "Dados comportamentais",
                    "Validação extensa",
                ],
            },
        ],
    },
    "modelo_geracao_valor": {
        "name": "Modelo de Geração de Valor",
        "definition": "Clareza sobre como a solução cria, entrega e captura valor.",
        "measurable_indicators": [
            "Estrutura custos",
            "Fontes receita",
            "Business Model Canvas",
            "Projeções financeiras",
            "Viabilidade econômica",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum modelo ou modelo genérico sem clareza.",
                "indicators": ["Ausente", "Sem detalhamento", "Viabilidade não demonstrada"],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Modelo descrito, sem viabilidade comprovada.",
                "indicators": [
                    "Estrutura básica",
                    "Custos/receitas mencionados",
                    "Sem análise viabilidade",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Modelo validado com plano sustentável de geração de valor.",
                "indicators": [
                    "Modelo testado",
                    "Projeções detalhadas",
                    "Viabilidade comprovada",
                ],
            },
        ],
    },
    "vantagem_competitiva": {
        "name": "Vantagem Competitiva",
        "definition": "Elemento que torna solução difícil de copiar, gerando diferencial sustentável.",
        "measurable_indicators": [
            "Propriedade intelectual",
            "Know-how exclusivo",
            "Parcerias exclusivas",
            "Barreiras entrada",
            "Competências únicas",
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhuma vantagem ou diferenciais frágeis e replicáveis.",
                "indicators": [
                    "Facilmente replicável",
                    "Sem elementos únicos",
                    "Vantagens temporárias",
                ],
            },
            {
                "level": 2,
                "label": "Médio",
                "description": "Diferencial presente, mas instável.",
                "indicators": [
                    "Vantagem identificada",
                    "Sustentabilidade incerta",
                    "Barreira moderada",
                ],
            },
            {
                "level": 3,
                "label": "Bom",
                "description": "Vantagem competitiva robusta e comprovadamente sustentável.",
                "indicators": [
                    "Propriedade protegida",
                    "Recursos exclusivos",
                    "Difícil copiar",
                ],
            },
        ],
    },
}


def get_label_for_level(level: int) -> str:
    """Retorna o rótulo para um nível numérico (1-3)."""
    if level == 1:
        return "Ruim"
    elif level == 2:
        return "Médio"
    elif level == 3:
        return "Bom"
    else:
        raise ValueError(f"Nível inválido: {level}. Deve estar entre 1 e 3.")


__all__ = ["EVALUATION_CRITERIA", "get_label_for_level"]


def get_label_for_level(level: int) -> str:
    """Retorna o rótulo para um nível numérico (1-3)."""
    if level == 1:
        return "Ruim"
    elif level == 2:
        return "Médio"
    elif level == 3:
        return "Bom"
    else:
        raise ValueError(f"Nível inválido: {level}. Deve estar entre 1 e 3.")


__all__ = ["EVALUATION_CRITERIA", "get_label_for_level"]
