import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export interface AvCardData {
  name: string;
  level: number; // 1-5
  label?: string;
  justification: string;
  suggestion?: string;
}

interface AvCardProps {
  avCard: AvCardData;
}

const levelMap = [
  {
    min: 5,
    label: "Excelente",
    color: "bg-green-600 text-white",
    border: "border-l-green-600",
  },
  {
    min: 4,
    label: "Bom",
    color: "bg-green-600 text-white",
    border: "border-l-green-600",
  },
  {
    min: 3,
    label: "Mediano",
    color: "bg-yellow-600 text-white",
    border: "border-l-yellow-600",
  },
  {
    min: 2,
    label: "Ruim",
    color: "bg-red-500 text-white",
    border: "border-l-red-500",
  },
  {
    min: 1,
    label: "Péssimo",
    color: "bg-red-500 text-white",
    border: "border-l-red-500",
  },
];

const getLevelColor = (level: number) =>
  levelMap.find((l) => level >= l.min)?.color || "bg-red-500 text-white";

const getLevelBorderColor = (level: number) =>
  levelMap.find((l) => level >= l.min)?.border || "border-l-red-500";

const getLevelLabel = (level: number) =>
  levelMap.find((l) => level >= l.min)?.label || "Péssimo";

export const AvCard = ({ avCard }: AvCardProps) => {
  return (
    <Card
      className={cn(
        "border-l-4 transition-all hover:shadow-lg hover:shadow-primary/5",
        getLevelBorderColor(avCard.level)
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-foreground">
            {avCard.name}
          </h3>
          <Badge
            className={cn(
              "shrink-0 font-semibold",
              getLevelColor(avCard.level)
            )}
          >
            Nível {avCard.level} - {getLevelLabel(avCard.level)}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
            Justificativa
          </h4>
          <p className="text-sm leading-relaxed text-foreground/90">
            {avCard.justification}
          </p>
        </div>
        {avCard.suggestion && (
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              Sugestão de Melhoria
            </h4>
            <p className="text-sm leading-relaxed text-primary/90 font-medium">
              {avCard.suggestion}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
