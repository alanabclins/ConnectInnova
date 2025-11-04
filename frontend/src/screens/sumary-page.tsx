import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import AnalysisService from "@/services/analysis.service";
import {
  AIGeneratedSummary,
  LoadingSkeleton,
  ErrorMessage,
} from "@/components/AiGeneratedSumary";
import { toast } from "sonner";

interface AnalysisData {
  clarity_resum: string;
  inovation_grade_resum: string;
  social_impact_resum: string;
  tec_eco_viability_resum: string;
  application_potencial_resum: string;
}

interface ProjectFormData {
  project_title: string;
  project_description: string;
}

interface ResumResponse {
  message: string;
  resum_id: string;
  resums: AnalysisData;
}

const initiatedFullAnalyses = new Set<string>();

const SummaryPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { projectId, projectData } = (location.state || {}) as {
    projectId?: string;
    projectData?: ProjectFormData;
  };

  const [isSummaryLoading, setIsSummaryLoading] = useState(true);
  const [isAnalysisLoading, setIsAnalysisLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId || !projectData) {
      const msg =
        "Dados do projeto não encontrados. Por favor, volte e tente novamente.";
      toast.error(msg);
      setError(msg);
      setIsSummaryLoading(false);
      return;
    }

    setError(null);
    fetchSummary();
    setIsAnalysisLoading(false);
  }, [projectId, projectData]);

  const fetchFullAnalysis = async (id: string) => {
    if (initiatedFullAnalyses.has(id)) {
      return;
    }
    initiatedFullAnalyses.add(id);

    let analysisToastId;
    try {
      setIsAnalysisLoading(true);
      analysisToastId = toast.loading(
        "Finalizando análise detalhada. Isso pode levar um momento.",
        {
          description: "",
          duration: Infinity,
          id: "analysis-loading",
        }
      );

      await AnalysisService.generateFullAnalysis(id, true);

      toast.success("Análise detalhada concluída!", {
        description: "O dashboard está pronto. Você já pode navegar.",
        id: analysisToastId,
        duration: 15,
      });
    } catch (err) {
      console.error("Erro ao gerar análise completa:", err);

      initiatedFullAnalyses.delete(id);

      toast.error(
        "Falha ao gerar análise detalhada. O dashboard pode não carregar corretamente.",
        { id: analysisToastId }
      );
    } finally {
      setIsAnalysisLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      setIsSummaryLoading(true);
      const resumResponse: ResumResponse = await AnalysisService.resumAnalysis(
        projectId
      );

      if (resumResponse?.resums) {
        setAnalysis(resumResponse.resums);
        setError(null);
        fetchFullAnalysis(projectId);
      } else {
        throw new Error("O resumo da análise não foi encontrado.");
      }
    } catch (err) {
      console.error("Erro ao carregar resumo:", err);
      const msg =
        "Não foi possível carregar o resumo da análise. Verifique sua conexão.";
      toast.error(msg);
      setError(msg);
    } finally {
      setIsSummaryLoading(false);
    }
  };

  const handleGoToDashboard = () => {
    if (projectId && projectData && !isAnalysisLoading) {
      navigate(`/home/dashboard`, {
        state: {
          projectId: projectId,
          projectData: projectData,
        },
      });
    }
  };

  if (isSummaryLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={
          error ||
          "Ocorreu um erro inesperado e o resumo não pôde ser carregado."
        }
      />
    );
  }

  if (analysis && projectData) {
    return (
      <AIGeneratedSummary
        analysis={analysis}
        projectData={projectData}
        onGoToDashboard={handleGoToDashboard}
        isAnalysisLoading={isAnalysisLoading}
      />
    );
  }

  return <ErrorMessage message="Ocorreu um erro inesperado." />;
};

export default SummaryPage;
