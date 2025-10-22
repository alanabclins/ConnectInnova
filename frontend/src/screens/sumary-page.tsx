import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import AnalysisService from "@/services/analysis.service";
import {
  AIGeneratedSummary,
  LoadingSkeleton,
  ErrorMessage,
} from "@/components/AiGeneratedSumary"; 

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

const SummaryPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { projectId, projectData } = (location.state || {}) as {
    projectId?: string;
    projectData?: ProjectFormData;
  };

  const [isLoading, setIsLoading] = useState(true);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.documentElement.classList.add("dark");

    if (!projectId || !projectData) {
      setError(
        "Dados do projeto não encontrados. Por favor, volte e tente novamente."
      );
      setIsLoading(false);
      return;
    }

    const fetchProjectAnalysis = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const analysisResponse = await AnalysisService.analyzeProject(
          projectId
        );

        if (!analysisResponse?.resum_id) {
          throw new Error(
            "ID do resumo não encontrado na resposta da análise."
          );
        }

        const resumResponse = await AnalysisService.resumAnalysis(
          analysisResponse.resum_id
        );

        if (resumResponse && resumResponse.length > 0) {
          setAnalysis(resumResponse[0]);
        } else {
          throw new Error("O resumo da análise não foi encontrado.");
        }
      } catch (err) {
        console.error("Erro ao carregar análise:", err);
        setError(
          "Não foi possível carregar o resumo da análise. Tente novamente mais tarde."
        );
        setAnalysis(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjectAnalysis();
  }, [projectId, projectData]);

  const handleGoToDashboard = () => {
    if (projectId) {
      navigate(`/home/dashboard`, {
        state: { projectId: projectId },
      });
    }
  };

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (analysis && projectData) {
    return (
      <AIGeneratedSummary
        analysis={analysis}
        projectData={projectData}
        onGoToDashboard={handleGoToDashboard}
      />
    );
  }

  return <ErrorMessage message="Ocorreu um erro inesperado." />;
};

export default SummaryPage;
