import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { IconPlus } from "@tabler/icons-react";

export default function MyProjects() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-1 flex-col gap-6 p-6">
      {/* Título da página */}
      <h1 className="text-2xl font-semibold text-foreground mb-4">
        Meus Projetos
      </h1>

      {/* Grid de projetos */}
      <div className="grid auto-rows-min gap-5 md:grid-cols-3">
        {/* Botão de adicionar projeto */}
        <div
          onClick={() => navigate("/project-stories")}
          className="aspect-video rounded-xl border-2 border-dashed border-muted-foreground/30 flex items-center justify-center cursor-pointer hover:border-primary transition-colors duration-200"
        >
          <Button
            variant="ghost"
            size="icon"
            className="h-16 w-16 rounded-full bg-primary text-primary-foreground shadow-md hover:bg-primary/90 transition-all duration-200"
          >
            <IconPlus size={28} stroke={2} />
          </Button>
        </div>

        <div className="bg-muted/20 aspect-video rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200" />
        <div className="bg-muted/20 aspect-video rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200" />
      </div>

      <div className="bg-muted/20 min-h-[40vh] flex-1 rounded-xl shadow-sm transition-shadow duration-200" />
    </div>
  );
}
