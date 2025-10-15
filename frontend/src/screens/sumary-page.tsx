import { useEffect } from "react";
import { useLocation, useSearchParams } from "react-router-dom";
import { AIGeneratedSummary } from "@/components/AiGeneratedSumary";

const SummaryPage = () => {
  const location = useLocation();
  const [searchParams] = useSearchParams();

  // 1. Tenta pegar o ID pela URL (/summary?projectId=uuid)
  const projectIdFromQuery = searchParams.get("projectId");

  const state = location.state as { projectId?: string } | undefined;
  const projectIdFromState = state?.projectId;

  const projectId = projectIdFromQuery || projectIdFromState;

  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  if (!projectId) {
    return (
      <div className="text-center text-red-500 mt-10">
        Nenhum projeto foi encontrado. Passe um projectId válido para continuar.

      </div>
    );
  }

  return <AIGeneratedSummary projectId={projectId} />;
};

export default SummaryPage;
