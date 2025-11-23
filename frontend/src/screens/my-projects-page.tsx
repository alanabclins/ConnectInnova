import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { ProjectCard } from "@/components/project-card";
import { AddProjectCard } from "@/components/add-project-card";
import ProjectService from "@/services/project.service";
import { toast } from "sonner";
import LoadingSpinner from "@/components/loading-spinner";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"; // Import para o pop-up
import { Spinner } from "@/components/ui/shadcn-io/spinner";
import {
  clearProjectFormData,
  hasSavedProjectFormData,
} from "@/hooks/useProjectForm";

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

interface ProjectCardData {
  id: string; // Este será o UUID
  name: string;
  description: string;
  createdAt: string;
}

export default function MyProjects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<ProjectDetails[]>([]);
  const [loading, setLoading] = useState(true);

  // Estados para controlar o diálogo de deleção
  const [projectToDelete, setProjectToDelete] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDraftDialog, setShowDraftDialog] = useState(false);

  useEffect(() => {
    fetchProjects();
    if (hasSavedProjectFormData()) {
      setShowDraftDialog(true);
    }
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data: ProjectDetails[] = await ProjectService.getProjects();
      setProjects(data);
    } catch (error) {
      console.error("Erro ao carregar projetos:", error);
      toast.error("Erro ao carregar projetos. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddProject = () => navigate("project-stories");

  const handleProjectClick = (projectId: string, projectData: ProjectDetails) =>
    navigate(`/home/dashboard`, {
      state: { projectId, projectData },
    });

  // --- Funções de Deleção ---

  /** Abre o pop-up de confirmação */
  const handleDeleteClick = (projectId: string) => {
    setProjectToDelete(projectId);
  };

  /** Fecha o pop-up (seja por clique no Cancelar ou fora dele) */
  const handleCancelDelete = () => {
    if (isDeleting) return; // Impede o fechamento durante o loading
    setProjectToDelete(null);
  };

  /** Confirma e executa a exclusão */
  const handleConfirmDelete = async () => {
    if (!projectToDelete) return;

    setIsDeleting(true);
    try {
      await ProjectService.deleteProject(projectToDelete); // Usa o UUID
      toast.success("Projeto deletado com sucesso!");

      // Atualiza a lista de projetos na tela, removendo o que foi deletado
      setProjects((prevProjects) =>
        prevProjects.filter((p) => p.uuid !== projectToDelete)
      );
    } catch (error) {
      console.error("Erro ao deletar projeto:", error);
      toast.error("Erro ao deletar projeto. Tente novamente.");
    } finally {
      setIsDeleting(false);
      setProjectToDelete(null); // Fecha o pop-up
    }
  };

  // Mapeia os dados para os cards
  const projectCardData: (ProjectCardData & { fullData: ProjectDetails })[] =
    projects.map((p) => ({
      id: p.uuid, // Passando o UUID como 'id'
      name: p.project_title,
      description: p.project_description,
      createdAt: p.timestamp,
      fullData: p,
    }));

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <section className="flex flex-1 flex-col gap-8 p-8 md:mr-[6vh] lg:mr-0">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Meus Projetos</h1>
        <p className="text-muted-foreground"></p>
      </header>

      <div className="min-w-0">
        {projects.length === 0 ? (
          <div className="flex justify-start">
            <AddProjectCard onClick={handleAddProject} hasProjects={false} />
          </div>
        ) : (
          <Carousel opts={{ align: "start", loop: false }} className="min-w-0">
            <CarouselContent className="py-4 px-8">
              {projectCardData.map((project) => (
                <CarouselItem
                  key={project.id}
                  className="pl-4 basis-full md:basis-1/1 lg:basis-1/3"
                >
                  <div className="h-full transition-all duration-300 ease-in-out hover:scale-[1.02] hover:z-10">
                    <ProjectCard
                      id={project.id}
                      name={project.name}
                      description={project.description}
                      createdAt={project.createdAt}
                      onClick={() =>
                        handleProjectClick(project.id, project.fullData)
                      }
                      onDelete={() => handleDeleteClick(project.id)}
                    />
                  </div>
                </CarouselItem>
              ))}

              <CarouselItem className="pl-4 basis-full md:basis-1/2 lg:basis-1/3">
                <div className="h-full transition-all duration-300 ease-in-out hover:scale-[1.02] hover:z-10">
                  <AddProjectCard onClick={handleAddProject} hasProjects />
                </div>
              </CarouselItem>
            </CarouselContent>
            <CarouselPrevious className="flex hidden md:flex left-[-2vh] rounded-full border border-border shadow-md transition-all hover:bg-primary hover:text-primary-foreground hover:scale-105" />
            <CarouselNext className="flex right-[-3vh] rounded-full border border-border shadow-md transition-all hover:bg-primary hover:text-primary-foreground hover:scale-105" />
          </Carousel>
        )}
      </div>

      <AlertDialog
        open={!!projectToDelete}
        onOpenChange={(open) => !open && handleCancelDelete()}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Você tem certeza?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta ação não pode ser desfeita. Isso excluirá permanentemente o
              seu projeto e todos os dados associados a ele.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel
              onClick={handleCancelDelete}
              disabled={isDeleting}
            >
              Cancelar
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmDelete}
              disabled={isDeleting}
              className="!bg-red-600 hover:bg-red-700 !text-white"
            >
              {isDeleting ? (
                <Spinner variant="ellipsis" size="sm" className="text-white" />
              ) : (
                "Sim, deletar"
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={showDraftDialog} onOpenChange={setShowDraftDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Você parou no meio do caminho</AlertDialogTitle>
            <AlertDialogDescription>
              Encontramos um rascunho salvo do seu projeto. Deseja continuar de
              onde parou ou iniciar um novo?
            </AlertDialogDescription>
          </AlertDialogHeader>

          <AlertDialogFooter>
            <AlertDialogCancel
              onClick={() => {
                clearProjectFormData();
                setShowDraftDialog(false);
              }}
            >
              Esquecer rascunho
            </AlertDialogCancel>

            <AlertDialogAction
              onClick={() => navigate("project-stories")}
              className="!bg-primary !text-primary-foreground hover:bg-primary/80"
            >
              Continuar de onde parei
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  );
}
