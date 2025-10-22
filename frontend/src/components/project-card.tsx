import { Card } from "@/components/ui/card";
import { IconCalendar, IconFileText } from "@tabler/icons-react";

interface ProjectCardProps {
  id: string;
  name: string;
  description?: string;
  createdAt?: string;
  onClick?: () => void;
}

export const ProjectCard = ({
  name,
  description,
  createdAt,
  onClick,
}: ProjectCardProps) => {
  return (
    <Card
      onClick={onClick}
      className="w-full h-full max-h-48 cursor-pointer bg-card hover:bg-card/90 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg overflow-hidden group flex flex-col"
    >
      <div className="flex flex-col justify-between flex-1 px-6">
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <IconFileText className="w-5 h-5 text-primary mt-1 flex-shrink-0" />
            <h3 className="text-lg font-semibold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
              {name}
            </h3>
          </div>
          {description && (
            <p className="text-sm text-muted-foreground line-clamp-3 leading-relaxed">
              {description}
            </p>
          )}
        </div>

        {createdAt && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-4">
            <IconCalendar className="w-4 h-4" />
            <span>{new Date(createdAt).toLocaleDateString("pt-BR")}</span>
          </div>
        )}
      </div>
    </Card>
  );
};
