import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { AIGeneratedSummary } from "@/components/AiGeneratedSumary";

const SummaryPage = () => {
  const location = useLocation();

  // Recupera o projectId recebido pelo navigate(...)
  const { projectId, projectData } = (location.state || {}) as { projectId?: string, projectData?: any };

  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  if (!projectId) {
    return (
      <div className="flex items-center justify-center h-screen text-red-500 text-lg">
        Nenhum projeto foi encontrado. Certifique-se de passar um projectId ao navegar para esta página.
      </div>
    );
  }

  return <AIGeneratedSummary projectId={projectId} formsProjectData={projectData}/>;
};

export default SummaryPage;
