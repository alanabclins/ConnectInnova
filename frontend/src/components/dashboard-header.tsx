import { IconChevronLeft } from "@tabler/icons-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "./ui/separator";

interface DashboardHeaderProps {
  title: string;
  description: string;
  tags?: string[];
  onBack: () => void;
}

export const DashboardHeader = ({
  title,
  description,
  tags = [],
  onBack,
}: DashboardHeaderProps) => {
  return (
    <div>
      <div className="flex items-start gap-4 p-6 md:p-8">
        <Button
          variant="ghost"
          size="icon"
          onClick={onBack}
          className="shrink-0 text-primary-foreground hover:bg-primary-foreground/10"
        >
          <IconChevronLeft className="w-5 h-5" />
        </Button>

        <div className="flex-1 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center md:gap-4">
            <h1 className="text-2xl md:text-3xl font-bold text-primary-foreground">
              {title}
            </h1>
            <Separator
              orientation="vertical"
              className="hidden md:flex mx-4 data-[orientation=vertical]:h-7 border-[1px]"
            />
            <p className="text-sm md:text-base text-primary-foreground/90 leading-relaxed max-w-4xl break-words whitespace-pre-wrap">
              {description}
            </p>
          </div>

          {tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
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
    </div>
  );
};
