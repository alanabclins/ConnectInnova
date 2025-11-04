import { IconChevronLeft, IconEdit } from "@tabler/icons-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "./ui/separator";
import { EditButton } from "./edit-button";

interface DashboardHeaderProps {
  title: string;
  description: string;
  tags?: string[];
  onBack: () => void;
  onEdit?: () => void;
}

export const DashboardHeader = ({
  title,
  description,
  tags = [],
  onBack,
  onEdit,
}: DashboardHeaderProps) => {
  return (
    <div>
      <div className="flex flex-col items-start gap-4 p-6 md:p-8 w-full">
        <div className="flex-1 space-y-6 w-full">
          <div className="flex flex-col md:flex-row md:items-start gap-4 w-full">
            <Button
              variant="ghost"
              size="icon"
              onClick={onBack}
              className="shrink-0 text-primary-foreground hover:bg-primary-foreground/10"
            >
              <IconChevronLeft className="w-5 h-5" />
            </Button>

            <div className="flex justify-between items-center">
              <h1 className="text-2xl md:text-3xl font-bold text-primary-foreground break-words">
                {title}
              </h1>

              <div className="shrink-0 md:ml-auto block md:hidden">
                {onEdit && <EditButton onEdit={onEdit} />}
              </div>
            </div>

            <Separator
              orientation="vertical"
              className="hidden md:flex mx-4 data-[orientation=vertical]:h-7 border-[1px]"
            />
            <p className="flex-1 text-sm md:text-base text-primary-foreground/90 leading-relaxed max-w-4xl break-words whitespace-pre-wrap min-w-0">
              {description}
            </p>

            <div className="shrink-0 md:ml-auto hidden md:block">
              {onEdit && <EditButton onEdit={onEdit} />}
            </div>
          </div>
        </div>

        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 md:pl-[3.5rem] w-full">
            {tags.map((tag, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="bg-primary-foreground/20 text-primary-foreground border-primary-foreground/30"
              >
                #{tag}
              </Badge>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
