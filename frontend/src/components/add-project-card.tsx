import { Plus } from "lucide-react";
import { Card } from "@/components/ui/card";

interface AddProjectCardProps {
  onClick?: () => void;
  hasProjects?: boolean;
}

export const AddProjectCard = ({
  onClick,
  hasProjects,
}: AddProjectCardProps) => {
  return (
    <Card
      onClick={onClick}
      className="w-full h-full cursor-pointer border-2 border-dashed border-border hover:border-primary transition-all duration-300 bg-card/60 hover:bg-card/80 group flex flex-col items-center justify-center"
    >
      <div className="flex flex-col items-center justify-center gap-3 p-6">
        <div className="relative">
          <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl group-hover:blur-2xl transition-all duration-300" />
          <div className="relative h-16 w-16 rounded-full bg-primary flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-lg">
            <Plus
              className="w-8 h-8 text-primary-foreground"
              strokeWidth={2.5}
            />
          </div>
        </div>
        <div className="text-center space-y-1">
          <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
            Novo Projeto
          </p>
          {!hasProjects && (
            <p className="text-xs text-muted-foreground">Clique para começar</p>
          )}
        </div>
      </div>
    </Card>
  );
};
