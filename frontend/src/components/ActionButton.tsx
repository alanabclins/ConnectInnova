import React from "react";
import { Button } from "@/components/ui/button";
import { type TablerIcon } from "@tabler/icons-react";

interface ActionButtonProps {
  icon: TablerIcon;
  label: string;
  onClick?: () => void;
}

export const ActionButton: React.FC<ActionButtonProps> = ({
  icon: Icon,
  label,
  onClick,
}) => {
  return (
    <Button
      variant="secondary"
      size="sm"
      className="h-10 px-4 gap-2 bg-secondary hover:bg-secondary/80 text-secondary-foreground rounded-full"
      onClick={onClick}
    >
      <Icon className="w-4 h-4" />
      <span className="text-sm">{label}</span>
    </Button>
  );
};
