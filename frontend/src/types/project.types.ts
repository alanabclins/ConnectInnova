export interface CriterionDetail {
  level: number;
  label: string;
  feedback: string;
  improvement: string;
}

export interface CriteriaEvaluationContainer {
  proposta_de_valor: CriterionDetail;
  pertinencia_ao_problema: CriterionDetail;
  alinhamento_com_objetivos: CriterionDetail;
  adequacao_ao_contexto: CriterionDetail;
  originalidade: CriterionDetail;
  capacidade_de_diferenciacao: CriterionDetail;
  uso_inteligente_tecnologias: CriterionDetail;
  impacto_social_ambiental: CriterionDetail;
  escalabilidade: CriterionDetail;
  sustentabilidade: CriterionDetail;
  indicadores_de_sucesso: CriterionDetail;
  capacidade_de_melhoria: CriterionDetail;
  segmento_de_clientes: CriterionDetail;
  modelo_geracao_valor: CriterionDetail;
  vantagem_competitiva: CriterionDetail;
  [key: string]: CriterionDetail;
}

export interface RawAnalysisResponse {
  _id: string;
  uuid: string;
  project_id: string;
  student_id: string;
  feedback: {
    content: string;
    status: string;
    timestamp: string;
  };
  criteria_evaluation: CriteriaEvaluationContainer;
}

export interface ProjectDetails {
  _id: string;
  uuid: string;
  project_title: string;
  project_description: string;
  solution_proposal: string;
  student_id: string;
  timestamp: string;
  problem_description: string;
  target_audience: string;
  value_proposition: string;
  customer_segment: string;
  revenue_model: string;
  competitive_advantage: string;
  innovation: string;
  social_impact: string;
  technical_feasibility: string;
  scalability: string;
  who_are_you: string;
  academy_info: string;
  market_info: string;
  clarity_problem: string;
  inovation_grade: string;
  social_impact_aggregated: string;
  tec_eco_viability: string;
  application_potencial: string;
}

export interface AnalysisState {
  projectData: ProjectDetails;
  analysis: RawAnalysisResponse;
}