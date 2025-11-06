import { IconChevronLeft } from "@tabler/icons-react";
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
      <div className="flex flex-col items-start gap-4 p-6 lg:p-8 w-full">
        <div className="flex-1 space-y-6 w-full">
          <div className="flex flex-col lg:flex-row lg:items-start gap-4 w-full">
            <Button
              variant="ghost"
              size="icon"
              onClick={onBack}
              className="shrink-0 text-primary-foreground hover:bg-primary-foreground/10"
            >
              <IconChevronLeft className="w-5 h-5" />
            </Button>

            <div className="flex justify-between items-center">
              <h1 className="text-2xl lg:text-3xl font-bold text-primary-foreground break-words">
                {title}
              </h1>

              <div className="shrink-0 lg:ml-auto block lg:hidden">
                {onEdit && <EditButton onEdit={onEdit} />}
              </div>
            </div>

            <Separator
              orientation="vertical"
              className="hidden lg:flex mx-4 data-[orientation=vertical]:h-7 border-[1px]"
            />
            <p className="flex-1 text-sm lg:text-base text-primary-foreground/90 leading-relaxed max-w-4xl break-words whitespace-pre-wrap min-w-0">
              {description}
            </p>

            <div className="shrink-0 lg:ml-auto hidden lg:block">
              {onEdit && <EditButton onEdit={onEdit} />}
            </div>
          </div>
        </div>

        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 lg:pl-[3.5rem] w-full">
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
