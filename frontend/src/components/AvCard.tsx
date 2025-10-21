import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export interface AvCardData {
  name: string;
  level: number; // 1-5
  levelLabel: string; // "Ruim", "Médio", "Bom"
  justification: string;
  suggestion: string;
}

interface AvCardProps {
  avCard: AvCardData;
}

const getLevelColor = (level: number) => {
  if (level >= 4) return "bg-status-good text-white";
  if (level === 3) return "bg-status-medium text-white";
  return "bg-status-poor text-white";
};

const getLevelBorderColor = (level: number) => {
  if (level >= 4) return "border-l-status-good";
  if (level === 3) return "border-l-status-medium";
  return "border-l-status-poor";
};

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
            {" "}
            Nível {avCard.level} - {avCard.levelLabel}{" "}
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
