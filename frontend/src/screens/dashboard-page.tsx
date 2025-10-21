import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { AvCard, type AvCardData } from "@/components/AvCard";
import { toast } from "sonner";
import ProjectService from "@/services/project.service";
import { DashboardHeader } from "@/components/dashboard-header";
import { Spinner } from "@/components/ui/shadcn-io/spinner";

interface ProjectDetailsData {
  uuid: string;
  project_title: string;
  project_description: string;
  solution_proposal: string;
  clarity_problem: string;
  inovation_grade: string;
  social_impact: string;
  tec_eco_viability: string;
  application_potencial: string;
}

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { projectId } = (location.state || {}) as { projectId?: string };
  const [loading, setLoading] = useState(true);
  const [project, setProject] = useState<ProjectDetailsData | null>(null);

  useEffect(() => {
    loadProjectDetails();
  }, [projectId]);

  const loadProjectDetails = async () => {
    try {
      setLoading(true);
      // Busca todos os projetos e filtra pelo uuid
      const projects = await ProjectService.getProjects();
      console.log(projectId)
      const foundProject = projects.find((p: any) => p.uuid === projectId);

      if (foundProject) {
        setProject(foundProject);
      } else {
        toast.error("Projeto não encontrado");
        navigate("/");
      }
    } catch (error) {
      console.error("Erro ao carregar projeto:", error);
      toast.error("Erro ao carregar projeto. Tente novamente.");
      navigate("/");
    } finally {
      setLoading(false);
    }
  };

  // Mock data para os cards de avaliação (posteriormente virá da API)
  const avCards: AvCardData[] = [
    {
      name: "Clareza do Problema",
      level: 2,
      justification: project?.clarity_problem || "Aguardando análise...",
      suggestion:
        "Continue refinando a definição do problema para maior clareza.",
    },
    {
      name: "Grau de Inovação",
      level: 5,
      justification: project?.inovation_grade || "Aguardando análise...",
      suggestion: "Ótimo nível de inovação! Continue assim.",
    },
    {
      name: "Impacto Social",
      level: 4,
      justification: project?.social_impact || "Aguardando análise...",
      suggestion: "Considere expandir o alcance do impacto social.",
    },
    {
      name: "Viabilidade Técnica e Econômica",
      level: 3,
      justification: project?.tec_eco_viability || "Aguardando análise...",
      suggestion: "Revise os custos e recursos necessários para implementação.",
    },
    {
      name: "Potencial de Aplicação",
      level: 4,
      justification: project?.application_potencial || "Aguardando análise...",
      suggestion: "Explore mais casos de uso para aumentar o potencial.",
    },
  ];

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Spinner variant={"circle"} className="text-primary" />
      </div>
    );
  }

  if (!project) {
    return null;
  }

  return (
    <div className="flex flex-1 flex-col">
      <DashboardHeader
        title={project.project_title}
        description={project.project_description}
        tags={["Inovação", "Tecnologia", "Acadêmico"]}
        onBack={() => navigate("/")}
      />

      <div className="flex flex-1 flex-col gap-6 p-6 md:p-8">
        {/* Cards de avaliação em grid */}
        <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2">
          {avCards.map((avCard, index) => (
            <AvCard key={index} avCard={avCard} />
          ))}
        </div>
      </div>
    </div>
  );
}
