"""
TABELA DE NÍVEIS POR CRITÉRIO DE AVALIAÇÃO
===========================================

Este módulo documenta formalmente os critérios de avaliação de projetos,
incluindo definições, níveis (1-5), classificação (Ruim/Médio/Bom) e
indicadores mensuráveis para cada critério.

Estrutura de cada critério:
- Definição: Explicação clara do que o critério avalia
- Níveis: Descrições operacionais de cada nível (1-5)
- Classificação: Mapeamento dos níveis para rótulos qualitativos
- Indicadores: Sinais textuais e evidências mensuráveis que justificam cada nível

Classificação de Níveis:
- RUIM: Níveis 1-2 → Resposta incompleta, incoerente, genérica ou sem base
- MÉDIO: Nível 3 → Coerente, mas com falhas de clareza, validação ou aplicabilidade  
- BOM: Nível 4 → Bem estruturado, com evidências e aplicabilidade clara
- EXCELENTE: Nível 5 → Completo, validado, com evidências sólidas e impacto comprovado
"""

from typing import Dict, List, TypedDict


class CriterionLevel(TypedDict):
    """Estrutura de um nível de avaliação"""
    level: int
    label: str  # Ruim, Médio, Bom, Excelente
    description: str
    indicators: List[str]


class EvaluationCriterion(TypedDict):
    """Estrutura completa de um critério de avaliação"""
    name: str
    definition: str
    levels: List[CriterionLevel]
    measurable_indicators: List[str]


# =============================================================================
# CRITÉRIOS DE AVALIAÇÃO
# =============================================================================

EVALUATION_CRITERIA: Dict[str, EvaluationCriterion] = {

    "proposta_de_valor": {
        "name": "Proposta de Valor",
        "definition": (
            "Clareza sobre o benefício central entregue ao usuário e o diferencial "
            "da solução frente a alternativas existentes."
        ),
        "measurable_indicators": [
            "Evidência de problema validado com dados ou pesquisas",
            "Descrição clara e objetiva do valor entregue ao usuário",
            "Feedback de usuários reais ou potenciais",
            "Demonstração de diferencial em relação a concorrentes",
            "Protótipo funcional ou MVP testado"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": (
                    "Não apresenta claramente o problema nem o diferencial. "
                    "Falta definição do valor entregue ao usuário."
                ),
                "indicators": [
                    "Ausência de descrição do problema",
                    "Não menciona benefícios para o usuário",
                    "Não identifica diferenciais",
                    "Texto genérico e sem foco"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": (
                    "Descreve o problema de forma genérica, sem explicitar "
                    "o valor ou solução de forma clara."
                ),
                "indicators": [
                    "Problema descrito superficialmente",
                    "Valor não explicitado ou muito vago",
                    "Ausência de diferenciação clara",
                    "Falta de conexão entre problema e solução"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Problema e solução apresentados, mas com diferenciação "
                    "pouco evidente. Falta clareza no diferencial competitivo."
                ),
                "indicators": [
                    "Problema identificado mas sem dados de validação",
                    "Solução descrita de forma básica",
                    "Diferencial mencionado mas não fundamentado",
                    "Valor para o usuário não totalmente claro"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": (
                    "Problema e solução bem definidos, com diferencial claro "
                    "e relevante. Apresenta evidências iniciais de validação."
                ),
                "indicators": [
                    "Problema bem descrito com contexto",
                    "Solução detalhada e coerente",
                    "Diferencial claro e justificado",
                    "Valor para o usuário bem articulado",
                    "Presença de alguma evidência ou teste inicial"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Problema e solução sólidos, diferencial validado com evidências "
                    "concretas e percepção de valor clara pelos usuários."
                ),
                "indicators": [
                    "Problema validado com dados, entrevistas ou pesquisas",
                    "Solução detalhada com protótipo ou MVP",
                    "Diferencial comprovado com comparações",
                    "Feedback positivo de usuários reais",
                    "Métricas de valor demonstradas"
                ]
            }
        ]
    },

    "pertinencia_ao_problema": {
        "name": "Pertinência ao Problema",
        "definition": (
            "Grau em que a solução responde efetivamente à necessidade identificada."
        ),
        "measurable_indicators": [
            "Evidências de validação do problema (entrevistas, surveys, dados)",
            "Documentação de entrevistas com usuários",
            "Dados quantitativos ou qualitativos que comprovam a relevância",
            "Testes ou protótipos que abordam diretamente a dor identificada",
            "Feedback de stakeholders sobre a adequação da solução"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "A solução não se relaciona com o problema identificado.",
                "indicators": [
                    "Solução desconectada do problema apresentado",
                    "Ausência de relação lógica entre problema e solução",
                    "Não aborda a necessidade identificada"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": (
                    "Relaciona-se parcialmente, sem resolver o problema principal."
                ),
                "indicators": [
                    "Solução tangencial ao problema",
                    "Aborda aspectos secundários ignorando o core",
                    "Conexão fraca ou forçada"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Aborda o problema, mas de forma limitada ou superficial."
                ),
                "indicators": [
                    "Solução parcialmente adequada",
                    "Resolve parte do problema mas não todo",
                    "Falta profundidade na resolução"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Responde adequadamente à necessidade central.",
                "indicators": [
                    "Solução bem alinhada ao problema",
                    "Aborda os pontos principais identificados",
                    "Demonstra compreensão clara da necessidade"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Resolve o problema de forma consistente, comprovada com "
                    "dados ou feedback de usuários."
                ),
                "indicators": [
                    "Solução validada por usuários reais",
                    "Dados concretos de efetividade",
                    "Feedback positivo sobre resolução do problema",
                    "Testes comprovam adequação da solução"
                ]
            }
        ]
    },

    "alinhamento_com_objetivos": {
        "name": "Alinhamento com os Objetivos",
        "definition": (
            "Grau de coerência entre a solução proposta e os objetivos "
            "do projeto ou usuário."
        ),
        "measurable_indicators": [
            "Documentos formais de metas e objetivos",
            "Coerência entre entregas planejadas e objetivos definidos",
            "Métricas que mostram contribuição direta aos objetivos",
            "Análise de resultados alcançados vs. objetivos propostos",
            "Rastreabilidade entre funcionalidades e objetivos"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não está alinhada aos objetivos definidos.",
                "indicators": [
                    "Objetivos não mencionados ou ausentes",
                    "Solução não relacionada às metas",
                    "Desconexão total entre proposta e objetivos"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": (
                    "Alinhamento parcial, sem relação direta com as metas principais."
                ),
                "indicators": [
                    "Objetivos vagos ou genéricos",
                    "Conexão fraca entre solução e metas",
                    "Foco em objetivos secundários"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Atende parcialmente aos objetivos, sem detalhar como."
                ),
                "indicators": [
                    "Objetivos declarados mas sem detalhamento",
                    "Algum alinhamento visível mas incompleto",
                    "Falta clareza sobre como atingir os objetivos"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Alinhamento claro e coerente com as metas do projeto.",
                "indicators": [
                    "Objetivos bem definidos",
                    "Solução claramente conectada às metas",
                    "Explicação de como cada parte contribui",
                    "Rastreabilidade presente"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Alinhamento completo, com resultados e evidências que "
                    "demonstram contribuição direta aos objetivos."
                ),
                "indicators": [
                    "Objetivos mensuráveis e bem documentados",
                    "Métricas comprovam alinhamento",
                    "Resultados demonstrados para cada objetivo",
                    "Análise de impacto presente"
                ]
            }
        ]
    },

    "adequacao_ao_contexto": {
        "name": "Adequação ao Contexto",
        "definition": (
            "Grau de adaptação da solução às condições, público-alvo e "
            "restrições culturais, sociais ou técnicas."
        ),
        "measurable_indicators": [
            "Perfil detalhado do público-alvo (personas, demographics)",
            "Testes de usabilidade contextualizados",
            "Feedback contextualizado de usuários reais",
            "Documentação de adaptações culturais/sociais",
            "Análise de restrições técnicas e ambientais"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não considera o contexto nem o público-alvo.",
                "indicators": [
                    "Ausência de menção ao público-alvo",
                    "Não considera contexto de uso",
                    "Solução genérica sem adaptação"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Considera parcialmente o contexto, de forma genérica.",
                "indicators": [
                    "Menção superficial ao público",
                    "Contexto descrito vagamente",
                    "Poucas adaptações específicas"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Considera o público e ambiente, mas com pouca adaptação prática."
                ),
                "indicators": [
                    "Público identificado mas sem detalhes",
                    "Contexto mencionado mas não aprofundado",
                    "Adaptações mínimas"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Adapta-se adequadamente ao contexto e às restrições.",
                "indicators": [
                    "Público bem caracterizado",
                    "Contexto analisado em detalhes",
                    "Adaptações claras e justificadas",
                    "Considera restrições relevantes"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Totalmente adaptada, validada em campo com feedback contextualizado."
                ),
                "indicators": [
                    "Personas detalhadas e validadas",
                    "Testes em contexto real",
                    "Feedback contextualizado positivo",
                    "Adaptações comprovadamente efetivas"
                ]
            }
        ]
    },

    "originalidade": {
        "name": "Originalidade",
        "definition": (
            "Grau de inovação ou aprimoramento apresentado pela solução."
        ),
        "measurable_indicators": [
            "Análise comparativa com soluções existentes",
            "Uso de tecnologias ou abordagens inéditas",
            "Reconhecimento de inovação (prêmios, publicações, patentes)",
            "Evidências de diferenciação técnica ou metodológica",
            "Feedback externo sobre o caráter inovador"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Cópia direta de soluções existentes.",
                "indicators": [
                    "Reprodução de solução conhecida",
                    "Ausência de elementos novos",
                    "Não apresenta inovação"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Pequenas variações sem impacto significativo.",
                "indicators": [
                    "Modificações cosméticas",
                    "Variações irrelevantes",
                    "Baixo grau de novidade"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Introduz elementos novos, mas sem grande diferenciação."
                ),
                "indicators": [
                    "Alguns elementos inovadores",
                    "Combinação de ideias existentes",
                    "Inovação incremental"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Apresenta inovação relevante e aplicável.",
                "indicators": [
                    "Abordagem ou tecnologia diferenciada",
                    "Inovação clara e justificada",
                    "Aplicabilidade prática da inovação"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Solução criativa e disruptiva, reconhecida por sua "
                    "originalidade e impacto."
                ),
                "indicators": [
                    "Inovação radical ou disruptiva",
                    "Reconhecimento externo",
                    "Potencial de transformação do mercado/área",
                    "Originalidade comprovada e documentada"
                ]
            }
        ]
    },

    "capacidade_de_diferenciacao": {
        "name": "Capacidade de Diferenciação",
        "definition": (
            "Grau em que a solução se destaca em relação a alternativas existentes."
        ),
        "measurable_indicators": [
            "Análise de benchmarking com concorrentes",
            "Pesquisa de percepção de valor pelos usuários",
            "Evidências de desempenho superior (métricas comparativas)",
            "Documentação de diferenciais técnicos ou funcionais",
            "Feedback comparativo de usuários"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum diferencial identificável.",
                "indicators": [
                    "Sem distinção de outras soluções",
                    "Não menciona diferenciais",
                    "Igual a alternativas existentes"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Diferenciais pouco claros ou irrelevantes.",
                "indicators": [
                    "Diferenciais mencionados mas vagos",
                    "Distinções superficiais",
                    "Baixa relevância dos diferenciais"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": (
                    "Diferenciais moderados, perceptíveis apenas em alguns aspectos."
                ),
                "indicators": [
                    "Alguns diferenciais identificados",
                    "Distinção parcial",
                    "Relevância moderada"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Diferenciais claros e relevantes ao público-alvo.",
                "indicators": [
                    "Diferenciais bem definidos",
                    "Relevância clara para usuários",
                    "Comparação favorável com alternativas",
                    "Justificativa sólida dos diferenciais"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Diferenciais sólidos, sustentados por evidências e "
                    "percepção positiva dos usuários."
                ),
                "indicators": [
                    "Diferenciais comprovados com dados",
                    "Percepção positiva validada",
                    "Superioridade demonstrada",
                    "Reconhecimento externo dos diferenciais"
                ]
            }
        ]
    },

    "uso_inteligente_tecnologias": {
        "name": "Uso Inteligente de Tecnologias ou Métodos",
        "definition": (
            "Integração estratégica de tecnologias, técnicas ou metodologias "
            "para potencializar a solução."
        ),
        "measurable_indicators": [
            "Justificativa técnica das escolhas tecnológicas",
            "Documentação de frameworks, ferramentas e arquiteturas utilizadas",
            "Presença de protótipos ou implementações funcionais",
            "Evidências de eficiência técnica (performance, escalabilidade)",
            "Análise de trade-offs tecnológicos"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Uso inadequado ou inexistente de métodos/tecnologias.",
                "indicators": [
                    "Tecnologias não mencionadas",
                    "Escolhas inadequadas ao problema",
                    "Ausência de fundamentação técnica"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Uso básico, sem justificativa.",
                "indicators": [
                    "Tecnologias mencionadas superficialmente",
                    "Sem explicação das escolhas",
                    "Uso genérico sem otimização"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Uso adequado, mas com pouca otimização.",
                "indicators": [
                    "Tecnologias apropriadas",
                    "Justificativa básica presente",
                    "Oportunidades de otimização não exploradas"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Utiliza tecnologias de forma eficaz e justificada.",
                "indicators": [
                    "Escolhas tecnológicas bem fundamentadas",
                    "Uso eficiente demonstrado",
                    "Integração coerente de tecnologias",
                    "Considerações de trade-offs"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Integra de maneira inovadora, estratégica e "
                    "comprovadamente eficaz."
                ),
                "indicators": [
                    "Uso estratégico e otimizado",
                    "Inovação na aplicação tecnológica",
                    "Eficácia comprovada com métricas",
                    "Referência técnica na área"
                ]
            }
        ]
    },

    "impacto_social_ambiental": {
        "name": "Impacto Social ou Ambiental",
        "definition": (
            "Grau de benefício concreto gerado para pessoas, comunidades "
            "ou meio ambiente."
        ),
        "measurable_indicators": [
            "Dados quantitativos de impacto (pessoas beneficiadas, recursos economizados)",
            "Resultados qualitativos documentados (testemunhos, casos de uso)",
            "Alcance e escala de beneficiários",
            "Feedback de comunidades ou stakeholders impactados",
            "Métricas de impacto social/ambiental (ODS, indicadores ESG)"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum impacto identificável.",
                "indicators": [
                    "Não menciona impacto social/ambiental",
                    "Sem evidência de benefícios",
                    "Foco apenas comercial/técnico"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Impacto potencial, mas sem evidência.",
                "indicators": [
                    "Impacto mencionado genericamente",
                    "Sem dados ou comprovação",
                    "Benefícios não demonstrados"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Impacto perceptível em pequena escala.",
                "indicators": [
                    "Alguns benefícios documentados",
                    "Impacto localizado",
                    "Evidências iniciais de benefícios"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Impacto relevante comprovado.",
                "indicators": [
                    "Impacto bem documentado",
                    "Dados de beneficiários",
                    "Evidências claras de benefícios",
                    "Feedback positivo de impactados"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Impacto significativo e mensurado com evidências concretas."
                ),
                "indicators": [
                    "Impacto quantificado com métricas",
                    "Grande alcance comprovado",
                    "Reconhecimento externo do impacto",
                    "Transformação demonstrada"
                ]
            }
        ]
    },

    "escalabilidade": {
        "name": "Escalabilidade",
        "definition": (
            "Potencial da solução de ser ampliada ou replicada em outros contextos."
        ),
        "measurable_indicators": [
            "Existência de modelo de negócio ou operacional replicável",
            "Documentação de processos e procedimentos",
            "Evidências de testes em múltiplos contextos",
            "Análise de requisitos para expansão",
            "Casos de replicação bem-sucedida"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não pode ser replicada.",
                "indicators": [
                    "Solução única e não transferível",
                    "Dependência total de contexto específico",
                    "Sem possibilidade de expansão"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Replicação possível, mas sem estrutura.",
                "indicators": [
                    "Escalabilidade não considerada",
                    "Ausência de documentação para replicação",
                    "Muitas barreiras para expansão"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Escalável com adaptações significativas.",
                "indicators": [
                    "Possível replicar com ajustes",
                    "Alguma documentação presente",
                    "Escalabilidade limitada"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Pode ser replicada com ajustes mínimos.",
                "indicators": [
                    "Modelo replicável bem definido",
                    "Documentação adequada",
                    "Processos padronizados",
                    "Viabilidade de expansão clara"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": "Altamente escalável, validada em novos contextos.",
                "indicators": [
                    "Replicação comprovada",
                    "Documentação completa",
                    "Sucesso em múltiplos contextos",
                    "Infraestrutura para escala"
                ]
            }
        ]
    },

    "sustentabilidade": {
        "name": "Sustentabilidade",
        "definition": (
            "Capacidade de manter resultados e operações no longo prazo."
        ),
        "measurable_indicators": [
            "Plano financeiro ou modelo de sustentação",
            "Parcerias estratégicas estabelecidas",
            "Engajamento contínuo de stakeholders",
            "Indicadores de viabilidade financeira",
            "Estratégias de manutenção e continuidade"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não se mantém sem apoio externo constante.",
                "indicators": [
                    "Dependência total de financiamento externo",
                    "Sem plano de continuidade",
                    "Inviabilidade no longo prazo"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Sustentável apenas no curto prazo.",
                "indicators": [
                    "Viabilidade temporária",
                    "Sem estratégia de longo prazo",
                    "Recursos limitados"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Estratégias parciais de continuidade.",
                "indicators": [
                    "Algum planejamento de sustentação",
                    "Recursos identificados mas não garantidos",
                    "Sustentabilidade incerta"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Estrutura sólida para longo prazo.",
                "indicators": [
                    "Plano de sustentação definido",
                    "Fontes de recursos identificadas",
                    "Parcerias em desenvolvimento",
                    "Viabilidade demonstrada"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Sustentabilidade comprovada com planos e parceiros consolidados."
                ),
                "indicators": [
                    "Modelo financeiro validado",
                    "Parcerias estabelecidas",
                    "Autossustentabilidade demonstrada",
                    "Planejamento de longo prazo robusto"
                ]
            }
        ]
    },

    "indicadores_de_sucesso": {
        "name": "Indicadores de Sucesso",
        "definition": (
            "Existência de métricas e instrumentos para mensurar resultados e impactos."
        ),
        "measurable_indicators": [
            "KPIs (Key Performance Indicators) claramente definidos",
            "Métricas de desempenho quantificáveis",
            "Relatórios de resultados periódicos",
            "Sistema de monitoramento contínuo",
            "Dashboards ou ferramentas de acompanhamento"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhuma métrica definida.",
                "indicators": [
                    "Ausência total de métricas",
                    "Não menciona indicadores",
                    "Sem forma de medir sucesso"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Métricas genéricas e não aplicadas.",
                "indicators": [
                    "Métricas vagas ou irrelevantes",
                    "Não foram coletadas",
                    "Sem metodologia de medição"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Métricas definidas, mas sem mensuração.",
                "indicators": [
                    "KPIs identificados",
                    "Não há coleta sistemática",
                    "Mensuração incompleta"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Métricas aplicadas parcialmente.",
                "indicators": [
                    "KPIs bem definidos",
                    "Coleta de dados iniciada",
                    "Alguns resultados disponíveis",
                    "Processo de medição em andamento"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Métricas aplicadas e analisadas com resultados documentados."
                ),
                "indicators": [
                    "Sistema completo de métricas",
                    "Dados coletados continuamente",
                    "Análises regulares",
                    "Resultados documentados e analisados",
                    "Dashboards ou relatórios disponíveis"
                ]
            }
        ]
    },

    "capacidade_de_melhoria": {
        "name": "Capacidade de Melhoria",
        "definition": (
            "Grau em que a solução permite aprendizado, ajustes e evolução contínua."
        ),
        "measurable_indicators": [
            "Utilização documentada de feedback de usuários",
            "Histórico de iterações e versões",
            "Planos de melhoria estruturados",
            "Documentação de mudanças e evolução",
            "Processos ágeis ou metodologias iterativas"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Não permite ajustes.",
                "indicators": [
                    "Solução rígida",
                    "Não considera feedback",
                    "Sem evolução planejada"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Recebe feedback, mas não aplica.",
                "indicators": [
                    "Feedback coletado mas ignorado",
                    "Sem processo de melhoria",
                    "Resistência a mudanças"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Melhora pontualmente sem processo estruturado.",
                "indicators": [
                    "Algumas melhorias implementadas",
                    "Processo ad-hoc",
                    "Falta sistematização"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Possui processo ativo de aprimoramento.",
                "indicators": [
                    "Processo de melhoria definido",
                    "Feedback incorporado regularmente",
                    "Iterações documentadas",
                    "Ciclos de melhoria visíveis"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Cultura contínua de melhoria com base em dados e feedback."
                ),
                "indicators": [
                    "Cultura de melhoria contínua",
                    "Dados direcionam evoluções",
                    "Histórico robusto de iterações",
                    "Metodologia ágil aplicada",
                    "Aprendizado sistemático"
                ]
            }
        ]
    },

    "segmento_de_clientes": {
        "name": "Segmento de Clientes",
        "definition": (
            "Clareza e coerência na definição do público-alvo da solução."
        ),
        "measurable_indicators": [
            "Personas detalhadas e documentadas",
            "Dados de segmentação demográfica e comportamental",
            "Validação direta com público-alvo",
            "Testes de usabilidade com usuários reais",
            "Pesquisas de mercado ou perfil de usuário"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Público não definido.",
                "indicators": [
                    "Ausência de definição de público",
                    "Não menciona usuários-alvo",
                    "Falta total de segmentação"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Público genérico, sem dados.",
                "indicators": [
                    "Descrição vaga do público",
                    "Sem dados demográficos",
                    "Segmentação superficial"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Público identificado, mas sem validação.",
                "indicators": [
                    "Segmento identificado",
                    "Descrição básica presente",
                    "Falta validação com usuários reais"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Segmento definido e embasado em dados.",
                "indicators": [
                    "Público bem caracterizado",
                    "Dados demográficos presentes",
                    "Personas desenvolvidas",
                    "Alguma validação realizada"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Segmentos validados e detalhados com personas e comportamentos."
                ),
                "indicators": [
                    "Personas completas e validadas",
                    "Dados comportamentais ricos",
                    "Validação extensa com usuários",
                    "Segmentação precisa e comprovada"
                ]
            }
        ]
    },

    "modelo_geracao_valor": {
        "name": "Modelo de Geração de Valor (ou Viabilidade do Modelo de Negócio)",
        "definition": (
            "Clareza sobre como a solução cria, entrega e captura valor."
        ),
        "measurable_indicators": [
            "Estrutura de custos documentada",
            "Fontes de receita identificadas e analisadas",
            "Canvas de modelo de negócio (Business Model Canvas)",
            "Simulações financeiras ou projeções",
            "Análise de viabilidade econômica"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhum modelo definido.",
                "indicators": [
                    "Ausência de modelo de negócio",
                    "Não menciona geração de valor",
                    "Sem análise financeira"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Modelo genérico, sem clareza sobre geração de valor.",
                "indicators": [
                    "Modelo vago ou incompleto",
                    "Sem detalhamento de receitas/custos",
                    "Viabilidade não demonstrada"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Modelo descrito, mas sem viabilidade comprovada.",
                "indicators": [
                    "Estrutura básica presente",
                    "Custos e receitas mencionados",
                    "Falta análise de viabilidade"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": "Modelo coerente, com estimativas básicas.",
                "indicators": [
                    "Modelo bem estruturado",
                    "Estimativas financeiras presentes",
                    "Lógica de geração de valor clara",
                    "Análise preliminar de viabilidade"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Modelo validado e com plano de geração de valor sustentável."
                ),
                "indicators": [
                    "Modelo completo e testado",
                    "Projeções financeiras detalhadas",
                    "Validação de mercado",
                    "Viabilidade comprovada",
                    "Plano de captura de valor claro"
                ]
            }
        ]
    },

    "vantagem_competitiva": {
        "name": "Vantagem Competitiva (ou Vantagem Injusta)",
        "definition": (
            "Elemento que torna a solução difícil de ser copiada, "
            "gerando diferencial sustentável."
        ),
        "measurable_indicators": [
            "Propriedade intelectual (patentes, marcas registradas)",
            "Know-how exclusivo documentado",
            "Parcerias estratégicas exclusivas",
            "Barreiras de entrada documentadas",
            "Recursos ou competências únicas"
        ],
        "levels": [
            {
                "level": 1,
                "label": "Ruim",
                "description": "Nenhuma vantagem identificável.",
                "indicators": [
                    "Facilmente replicável",
                    "Sem elementos únicos",
                    "Ausência de barreiras"
                ]
            },
            {
                "level": 2,
                "label": "Ruim",
                "description": "Diferenciais frágeis e replicáveis.",
                "indicators": [
                    "Vantagens temporárias",
                    "Baixa barreira de entrada",
                    "Fácil imitação"
                ]
            },
            {
                "level": 3,
                "label": "Médio",
                "description": "Diferencial presente, mas instável.",
                "indicators": [
                    "Alguma vantagem identificada",
                    "Sustentabilidade incerta",
                    "Barreira moderada"
                ]
            },
            {
                "level": 4,
                "label": "Bom",
                "description": (
                    "Diferencial claro e apoiado por competências exclusivas."
                ),
                "indicators": [
                    "Vantagem bem definida",
                    "Competências únicas",
                    "Difícil de replicar",
                    "Barreira significativa"
                ]
            },
            {
                "level": 5,
                "label": "Excelente",
                "description": (
                    "Vantagem competitiva robusta e comprovadamente sustentável."
                ),
                "indicators": [
                    "Propriedade intelectual protegida",
                    "Recursos exclusivos",
                    "Parcerias estratégicas",
                    "Barreira forte comprovada",
                    "Difícil ou impossível de copiar"
                ]
            }
        ]
    }
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_criterion(criterion_key: str) -> EvaluationCriterion:
    """
    Retorna um critério específico por sua chave.
    
    Args:
        criterion_key: Chave do critério (ex: 'proposta_de_valor')
        
    Returns:
        Dicionário com a estrutura completa do critério
        
    Raises:
        KeyError: Se o critério não existir
    """
    if criterion_key not in EVALUATION_CRITERIA:
        raise KeyError(f"Critério '{criterion_key}' não encontrado.")
    return EVALUATION_CRITERIA[criterion_key]


def get_level_description(criterion_key: str, level: int) -> CriterionLevel:
    """
    Retorna a descrição de um nível específico de um critério.
    
    Args:
        criterion_key: Chave do critério
        level: Nível de 1 a 5
        
    Returns:
        Dicionário com informações do nível
        
    Raises:
        KeyError: Se o critério não existir
        ValueError: Se o nível for inválido
    """
    criterion = get_criterion(criterion_key)

    if not 1 <= level <= 5:
        raise ValueError(f"Nível deve estar entre 1 e 5, recebido: {level}")

    for level_data in criterion["levels"]:
        if level_data["level"] == level:
            return level_data

    raise ValueError(f"Nível {level} não encontrado para o critério '{criterion_key}'")


def get_label_for_level(level: int) -> str:
    """
    Retorna o rótulo qualitativo para um nível numérico.
    
    Args:
        level: Nível de 1 a 5
        
    Returns:
        String com rótulo: "Ruim", "Médio", "Bom", ou "Excelente"
    """
    if level in [1, 2]:
        return "Ruim"
    elif level == 3:
        return "Médio"
    elif level == 4:
        return "Bom"
    elif level == 5:
        return "Excelente"
    else:
        raise ValueError(f"Nível inválido: {level}. Deve estar entre 1 e 5.")


def list_all_criteria() -> List[str]:
    """
    Retorna lista com nomes de todos os critérios disponíveis.
    
    Returns:
        Lista de strings com nomes dos critérios
    """
    return [criterion["name"] for criterion in EVALUATION_CRITERIA.values()]


def get_criteria_keys() -> List[str]:
    """
    Retorna lista com as chaves de todos os critérios.
    
    Returns:
        Lista de strings com chaves dos critérios
    """
    return list(EVALUATION_CRITERIA.keys())


# =============================================================================
# EXPORTAÇÃO
# =============================================================================

__all__ = [
    "EVALUATION_CRITERIA",
    "EvaluationCriterion",
    "CriterionLevel",
    "get_criterion",
    "get_level_description",
    "get_label_for_level",
    "list_all_criteria",
    "get_criteria_keys",
]

