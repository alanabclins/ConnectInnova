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
import { Spinner } from "@/components/ui/shadcn-io/spinner";

interface Project {
  id: string;
  name: string;
  description?: string;
  createdAt?: string;
}

interface ProjectResponse {
  uuid: string;
  project_title: string;
  project_description: string;
  timestamp: string;
}

export default function MyProjects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data: ProjectResponse[] = await ProjectService.getProjects();

      const mapped = data.map((p) => ({
        id: p.uuid,
        name: p.project_title,
        description: p.project_description,
        createdAt: p.timestamp,
      }));

      setProjects(mapped);
    } catch (error) {
      console.error("Erro ao carregar projetos:", error);
      toast.error("Erro ao carregar projetos. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddProject = () => navigate("project-stories");
  const handleProjectClick = (id: string) =>
    navigate(`/home/dashboard`, {
      state: { projectId: id },
    });

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Spinner variant={"circle"} className="text-primary"/>
      </div>
    );
  }

  return (
    <section className="flex flex-1 flex-col gap-8 p-6 md:p-8">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Meus Projetos</h1>
        <p className="text-muted-foreground">
          {projects.length > 0
            ? `Você tem ${projects.length} ${
                projects.length === 1 ? "projeto" : "projetos"
              }`
            : "Comece criando seu primeiro projeto"}
        </p>
      </header>

      <div className="w-full mx-auto md:px-3">
        {projects.length === 0 ? (
          <div className="flex justify-start">
            <AddProjectCard onClick={handleAddProject} hasProjects={false} />
          </div>
        ) : (
          <Carousel
            opts={{ align: "start", loop: false }}
            className="w-full h-48"
          >
            <CarouselContent className="-ml-2 py-4">
              {projects.map((project) => (
                <CarouselItem
                  key={project.id}
                  className="pl-4 md:basis-1/2 lg:basis-1/3"
                >
                  <div className="h-full transition-all duration-300 ease-in-out hover:scale-[1.02] hover:z-10">
                    <ProjectCard
                      {...project}
                      onClick={() => handleProjectClick(project.id)}
                    />
                  </div>
                </CarouselItem>
              ))}

              <CarouselItem className="md:basis-1/2 lg:basis-1/3">
                <div className="h-full transition-all duration-300 ease-in-out hover:scale-[1.02] hover:z-10">
                  <AddProjectCard onClick={handleAddProject} hasProjects />
                </div>
              </CarouselItem>
            </CarouselContent>

            <CarouselPrevious className="hidden md:flex rounded-full border border-border shadow-md transition-all hover:bg-primary hover:text-primary-foreground hover:scale-105" />
            <CarouselNext className="hidden md:flex rounded-full border border-border shadow-md transition-all hover:bg-primary hover:text-primary-foreground hover:scale-105" />
          </Carousel>
        )}
      </div>
    </section>
  );
}
