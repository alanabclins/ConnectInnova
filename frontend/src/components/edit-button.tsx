import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { IconEdit } from "@tabler/icons-react";

export function EditButton({ onEdit }: { onEdit: () => void }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="outline"
            size="icon-lg"
            onClick={onEdit}
            className="bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <IconEdit className="w-5 h-5" />
          </Button>
        </TooltipTrigger>
        <TooltipContent side="left">
          <p>Editar projeto</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
