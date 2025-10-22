import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { IconSparkles, IconCheck, IconPlus, IconLoader2 } from "@tabler/icons-react";

interface AnalysisData {
  clarity_resum: string;
  inovation_grade_resum: string;
  social_impact_resum: string;
  tec_eco_viability_resum: string;
  application_potencial_resum: string;
}

interface ProjectFormData {
  project_title: string;
  project_description: string;
}

interface AIGeneratedSummaryProps {
  analysis: AnalysisData;
  projectData: ProjectFormData;
  onGoToDashboard: () => void;
  isAnalysisLoading: boolean;
}

export const AIGeneratedSummary: React.FC<AIGeneratedSummaryProps> = ({
  analysis,
  projectData,
  onGoToDashboard,
  isAnalysisLoading,
}) => {
  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-3xl mx-auto space-y-4">
        <HeaderCard data={projectData} />

        <Card className="p-4 md:p-6">
          <h2 className="text-lg font-semibold mb-4 text-foreground">
            Resumos gerados pela IA
          </h2>

          <SummaryItem
            title="Clareza do Projeto"
            text={analysis.clarity_resum}
          />
          <SummaryItem
            title="Grau de Inovação"
            text={analysis.inovation_grade_resum}
          />
          <SummaryItem
            title="Impacto Social"
            text={analysis.social_impact_resum}
          />
          <SummaryItem
            title="Viabilidade Técnica e Econômica"
            text={analysis.tec_eco_viability_resum}
          />
          <SummaryItem
            title="Potencial de Aplicação"
            text={analysis.application_potencial_resum}
          />
        </Card>

        <div className="pt-4 pb-8">
          <Button
            onClick={onGoToDashboard}
            disabled={isAnalysisLoading}
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-6 text-base font-medium"
          >
            {isAnalysisLoading ? (
              <>
                <IconLoader2 className="w-5 h-5 mr-2 animate-spin" />
                Finalizando análise detalhada...
              </>
            ) : (
              <>
                <IconSparkles className="w-5 h-5 mr-2" />
                Ir para o dashboard
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

// ---------------------- Componentes Auxiliares ----------------------

const HeaderCard: React.FC<{ data: ProjectFormData }> = ({ data }) => (
  <Card className="p-4 md:p-6">
    <div className="flex items-start justify-between gap-4 mb-3">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 md:w-10 md:h-10 bg-success rounded-lg flex items-center justify-center flex-shrink-0">
          <IconCheck className="w-5 h-5 md:w-6 md:h-6 text-success-foreground" />
        </div>
        <div>
          <h1 className="text-xl md:text-2xl font-bold text-foreground">
            {data?.project_title || "Projeto Validado"}
          </h1>
          <Badge
            variant="outline"
            className="mt-1 text-xs border-success text-success"
          >
            <IconPlus className="w-3 h-3 mr-1" />
            Validado
          </Badge>
        </div>
      </div>
      <IconSparkles className="w-6 h-6 text-primary flex-shrink-0" />
    </div>

    <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
      {data?.project_description || "Descrição não disponível no momento."}
    </p>
  </Card>
);

const SummaryItem: React.FC<{ title: string; text?: string }> = ({
  title,
  text,
}) => (
  <div className="mb-4">
    <h3 className="font-semibold text-foreground mb-1">{title}</h3>
    <p className="text-sm text-muted-foreground leading-relaxed">
      {text || "Resumo ainda não disponível."}
    </p>
  </div>
);

export const ErrorMessage: React.FC<{ message: string }> = ({ message }) => (
  <div className="min-h-screen flex items-center justify-center text-center text-muted-foreground p-4">
    {message}
  </div>
);

const loadingStages = [
  "Analisando informações do projeto...",
  "Processando dados pessoais...",
  "Gerando insights...",
  "Finalizando resumo...",
];

export const LoadingSkeleton: React.FC = () => {
  const [stage, setStage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStage((prev) =>
        prev < loadingStages.length - 1 ? prev + 1 : prev
      );
    }, 1200);

    return () => clearInterval(interval);
  }, []);

  const progress = ((stage + 1) / loadingStages.length) * 100;

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <IconSparkles className="w-8 h-8 text-primary animate-pulse" />
            <h2 className="text-xl md:text-2xl font-bold">
              Gerando seu resumo...
            </h2>
          </div>

          <p className="text-sm md:text-base text-muted-foreground animate-pulse">
            {loadingStages[stage] || "Processando..."}
          </p>

          <div className="mt-4 max-w-md mx-auto h-2 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <Card key={i} className="p-4 md:p-6">
              <Skeleton className="h-6 w-1/2 mb-3" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-5/6 mb-2" />
              <Skeleton className="h-4 w-2/3" />
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};