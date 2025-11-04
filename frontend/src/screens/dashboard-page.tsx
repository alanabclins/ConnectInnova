import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";
import { AvCard, type AvCardData } from "@/components/AvCard";
import { toast } from "sonner";
import AnalysisService from "@/services/analysis.service";
import projectService from "@/services/project.service";
import { DashboardHeader } from "@/components/dashboard-header";
import LoadingSpinner from "@/components/loading-spinner";

import type {
  CriteriaEvaluationContainer,
  AnalysisState,
} from "@/types/project.types";

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

  const { projectId } = (location.state || {}) as {
    projectId: string;
  };

  const [loading, setLoading] = useState(true);
  const [analysisState, setAnalysisState] = useState<AnalysisState | null>(
    null
  );

  useEffect(() => {
    if (!projectId) {
      toast.error("ID do projeto não fornecido.");
      navigate("/home");
      return;
    }
    loadDashboardData();
  }, [projectId]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [analysisDetails, projectDetails] = await Promise.all([
        AnalysisService.getFeedback(projectId),
        projectService.getProjectDetails(projectId),
      ]);

      if (analysisDetails && projectDetails) {
        setAnalysisState({
          projectData: projectDetails,
          analysis: analysisDetails,
        });
      } else {
        toast.error("Análise ou dados do projeto não encontrados");
        navigate("/home");
      }
    } catch (error) {
      console.error("Erro ao carregar dados do dashboard:", error);
      toast.error("Erro ao carregar dados. Tente novamente.");
      navigate("/home");
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

    (
      Object.keys(CRITERIA_MAP) as (keyof CriteriaEvaluationContainer)[]
    ).forEach((key) => {
      const detail = criteria[key];
      const name = CRITERIA_MAP[key];

      if (detail && name) {
        cards.push({
          name: name,
          level: detail.level,
          justification: detail.feedback,
          suggestion: detail.improvement,
        });
      }
    });

    return cards;
  }, [analysis]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!project || !analysis) {
    return null;
  }

  const summaryContent =
    analysis.feedback?.content || project.project_description;

  return (
    <div className="flex flex-1 flex-col">
      <DashboardHeader
        title={project.project_title}
        description={project.project_description}
        tags={["Análise de IA", "Feedback", "15 Critérios"]}
        onBack={() => navigate("/home")}
        onEdit={() =>
          navigate("/home/project-stories", {
            state: {
              isEditing: true,
              projectToEdit: project,
            },
          })
        }
      />

      <div className="flex flex-1 flex-col gap-6 p-6 md:p-8">
        <h2 className="text-2xl font-bold text-foreground mt-4">
          Resumo da Análise
        </h2>
        <div className="text-lg text-muted-foreground p-4 rounded-md shadow-sm border border-border">
          {summaryContent}
        </div>

        <h2 className="text-2xl font-bold text-foreground mt-4">
          Avaliação Detalhada por Critério
        </h2>
        <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2 ">
          {avCards.map((avCard, index) => (
            <AvCard key={index} avCard={avCard} />
          ))}
        </div>
      </div>
    </div>
  );
}
