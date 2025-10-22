import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";
import { AvCard, type AvCardData } from "@/components/AvCard";
import { toast } from "sonner";
import analysisService from "@/services/analysis.service";
import { DashboardHeader } from "@/components/dashboard-header";
import { Spinner } from "@/components/ui/shadcn-io/spinner";

interface CriterionDetail {
  level: number;
  label: string;
  feedback: string;
}

interface CriteriaEvaluationContainer {
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

interface RawAnalysisResponse {
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

interface AnalysisState {
  projectData: ProjectDetails;
  analysis: RawAnalysisResponse;
}

const CRITERIA_MAP: { [key in keyof CriteriaEvaluationContainer]: string } = {
  proposta_de_valor: "Proposta de Valor",
  pertinencia_ao_problema: "Pertinência ao Problema",
  alinhamento_com_objetivos: "Alinhamento com Objetivos",
  adequacao_ao_contexto: "Adequação ao Contexto",
  originalidade: "Grau de Inovação",
  capacidade_de_diferenciacao: "Diferenciação",
  uso_inteligente_tecnologias: "Uso de Tecnologias",
  impacto_social_ambiental: "Impacto Social e Ambiental",
  escalabilidade: "Potencial de Aplicação",
  sustentabilidade: "Viabilidade Econômica e Sustentabilidade",
  indicadores_de_sucesso: "Métricas e Indicadores",
  capacidade_de_melhoria: "Capacidade de Melhoria Contínua",
  segmento_de_clientes: "Segmento de Clientes",
  modelo_geracao_valor: "Modelo de Geração de Valor",
  vantagem_competitiva: "Vantagem Competitiva",
};

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { projectId, projectData: initialProjectData } = (location.state || {}) as {
    projectId: string;
    projectData: ProjectDetails | undefined;
  };

  const [loading, setLoading] = useState(true);
  const [analysisState, setAnalysisState] = useState<AnalysisState | null>(null);

  useEffect(() => {
    if (!projectId || !initialProjectData) {
      toast.error("Detalhes do projeto não fornecidos.");
      navigate("/home/projects");
      return;
    }
    loadAnalysis();
  }, [projectId]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      const analysisDetails: RawAnalysisResponse = await analysisService.getFeedback(
        projectId,
        false
      );

      if (analysisDetails) {
        setAnalysisState({
          projectData: initialProjectData as ProjectDetails, 
          analysis: analysisDetails,
        });
      } else {
        toast.error("Análise do projeto não encontrada");
        navigate("/home/projects");
      }
    } catch (error) {
      console.error("Erro ao carregar análise:", error);
      toast.error("Erro ao carregar análise. Tente novamente.");
      navigate("/home/projects");
    } finally {
      setLoading(false);
    }
  };

  const analysis = analysisState?.analysis;
  const project = analysisState?.projectData;

  const avCards: AvCardData[] = useMemo(() => {
    if (!analysis) return [];

    const criteria = analysis.criteria_evaluation;
    const cards: AvCardData[] = [];

    (Object.keys(CRITERIA_MAP) as (keyof CriteriaEvaluationContainer)[]).forEach((key) => {
      const detail = criteria[key];
      const name = CRITERIA_MAP[key];

      cards.push({
        name: name,
        level: detail.level,
        justification: detail.feedback,
        suggestion: detail.feedback,
      });
    });

    return cards;
  }, [analysis]);


  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Spinner variant={"circle"} className="text-primary" />
      </div>
    );
  }

  if (!project || !analysis) {
    return null;
  }
  
  const summaryContent = analysis.feedback?.content || project.project_description;

  return (
    <div className="flex flex-1 flex-col">
      <DashboardHeader
        title={project.project_title}
        description={project.project_description}
        tags={["Análise de IA", "Feedback", "15 Critérios"]}
        onBack={() => navigate("/home")}
      />

      <div className="flex flex-1 flex-col gap-6 p-6 md:p-8">
        <h2 className="text-2xl font-bold text-foreground mt-4">Resumo da Análise</h2>
        <div className="text-lg text-muted-foreground p-4 rounded-md shadow-sm border border-border">
          {summaryContent}
        </div>
        
        <h2 className="text-2xl font-bold text-foreground mt-4">Avaliação Detalhada por Critério</h2>
        <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3">
          {avCards.map((avCard, index) => (
            <AvCard key={index} avCard={avCard} />
          ))}
        </div>
      </div>
    </div>
  );
}