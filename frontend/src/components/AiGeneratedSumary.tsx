import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { IconSparkles, IconCheck, IconPlus } from "@tabler/icons-react";
import { Progress } from "@/components/ui/progress";

interface AIGeneratedSummaryProps {
  projectData?: {
    title?: string;
    description?: string;
    solutionProposal?: string;
    socialImpact?: string;
    technicalFeasibility?: string;
    innovation?: string;
    whoAreYou?: string;
    academyInfo?: string;
    marketInfo?: string;
  };
  onRegenerate?: () => void;
}

export const AIGeneratedSummary: React.FC<AIGeneratedSummaryProps> = ({
  projectData,
  onRegenerate,
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [loadingStage, setLoadingStage] = useState(0);

  useEffect(() => {
    const stages = [
      "Analisando informações do projeto...",
      "Processando dados pessoais...",
      "Gerando insights...",
      "Finalizando resumo...",
    ];

    let currentStage = 0;
    const interval = setInterval(() => {
      if (currentStage < stages.length) {
        setLoadingStage(currentStage);
        currentStage++;
      } else {
        setIsLoading(false);
        clearInterval(interval);
      }
    }, 1200);

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return <LoadingSkeleton stage={loadingStage} />;
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-3xl mx-auto space-y-4">
        {/* Header Card */}
        <Card className="p-4 md:p-6">
          <div className="flex items-start justify-between gap-4 mb-3">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 md:w-10 md:h-10 bg-success rounded-lg flex items-center justify-center flex-shrink-0">
                <IconCheck className="w-5 h-5 md:w-6 md:h-6 text-success-foreground" />
              </div>
              <div>
                <h1 className="text-xl md:text-2xl font-bold text-foreground">
                  {projectData?.title || "AgroPlus"}
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
            {projectData?.description ||
              "O objetivo é criar uma solução inteligente criada no ambiente acadêmico para tornar a gestão de propriedades rurais mais eficiente e acessível."}
          </p>

          <p className="text-sm md:text-base text-muted-foreground leading-relaxed mt-3">
            {projectData?.solutionProposal ||
              "Solução trazendo sensores para o campo e dados claros do campo em tempo real para simplificar decisões. O diferencial está na sua usabilidade simplificada, validada com agricultores, pensado para uso de baixo custo. IA ajuda a identificar necessidades específicas, facilitando e otimizando certamente decisões de plantio, irrigação e colheita."}
          </p>
        </Card>

        {/* Classificação do projeto */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-semibold mb-4 text-foreground">
            Classificação do projeto
          </h2>

          <div className="space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-muted-foreground">
                Fase atual (observando horas dedicadas por semana)
              </span>
              <span className="font-medium text-foreground">MVP</span>
            </div>

            <div className="space-y-3">
              <MetricBar label="Lucide" value={8} max={10} />
              <MetricBar label="Node" value={7} max={10} />
              <MetricBar label="Drizzle" value={6} max={10} />
            </div>

            <div className="pt-3 border-t border-border">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">
                  Validação funcional
                </span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-success"></div>
                  <span className="font-medium text-foreground">Concluída</span>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Foco de desenvolvimento */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-semibold mb-3 text-foreground">
            Foco de desenvolvimento
          </h2>
          <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
            {projectData?.technicalFeasibility ||
              "Em andamento em 2 trajetórias: Coleta contínua de dados do campo em tempo real e Usabilidade e experiência do agricultor"}
          </p>
        </Card>

        {/* Proposta de Solução */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-bold mb-3">
            Proposta de solução
          </h2>
          <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
            Auxiliar pequenos e médios produtores na melhora da gestão agrícola
            e aumento da produtividade de forma sustentável.
          </p>
        </Card>

        {/* Ajustes em desenvolvimento */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-bold mb-4">
            Ajustes em desenvolvimento:
          </h2>
          <ul className="space-y-3">
            <BulletItem text="Inferência de soluções baseada em IA" />
            <BulletItem text="Coleta contínua de dados do campo em tempo real" />
            <BulletItem text="Usabilidade e experiência do agricultor" />
          </ul>
        </Card>

        {/* Próximos passos */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-bold mb-4">
            Próximos passos:
          </h2>
          <ul className="space-y-3">
            <BulletItem
              text="Estruturação do modelo de negócio"
              variant="success"
            />
            <BulletItem
              text="Refinamento técnico e validação de usabilidade"
              variant="success"
            />
            <BulletItem
              text="Parcerias estratégicas para entrada no mercado"
              variant="success"
            />
          </ul>
        </Card>

        {/* Sobre você */}
        <Card className="p-4 md:p-6">
          <h2 className="text-base md:text-lg font-semibold mb-4 text-foreground">
            Sobre você
          </h2>

          <div className="flex items-start gap-3 mb-4">
            <div className="w-12 h-12 md:w-14 md:h-14 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center flex-shrink-0">
              <span className="text-xl md:text-2xl font-bold text-white">
                {projectData?.whoAreYou?.charAt(0) || "L"}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="text-base md:text-lg font-bold text-foreground">
                  {projectData?.whoAreYou?.split(",")[0] || "Lucas"}
                </h3>
                <IconPlus className="w-5 h-5 text-primary flex-shrink-0" />
              </div>
              <p className="text-sm text-muted-foreground break-words">
                {projectData?.whoAreYou ||
                  "Lucas, estudante de Ciências da Computação da UFPR e morador de Altamira - PA. Identificou uma necessidade real durante sua vivência universitária e vida no campo."}
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4 pt-4 border-t border-border">
            <div>
              <h3 className="text-sm font-semibold mb-3 text-foreground">
                Experiência e habilidades:
              </h3>
              <div className="space-y-2">
                <SkillRow skill="Desenvolvimento de soluções" level={4} />
                <SkillRow skill="Tecnologias de IA/ML" level={3} />
                <SkillRow skill="Gestão de projetos" level={4} />
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold mb-2 text-foreground">
                Perfil pessoal e motivações:
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Vem de um contexto periférico da Região Norte • Motivado a gerar
                impacto social pela tecnologia • Cresceu em áreas rurais e
                pequenas, tendo contato com o campo • Sensibilizado por causas
                ambientais, equidade e economias sustentáveis • Hábil em
                compreender problemas, projetar e entregar soluções com
                agilidade
              </p>
            </div>
          </div>
        </Card>

        {/* Resumir Button */}
        <div className="pt-4 pb-8">
          <Button
            onClick={onRegenerate}
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-6 text-base font-medium"
          >
            <IconSparkles className="w-5 h-5 mr-2" />
            Resumir
          </Button>
        </div>
      </div>
    </div>
  );
};

// Metric Bar Component
const MetricBar: React.FC<{ label: string; value: number; max: number }> = ({
  label,
  value,
  max,
}) => {
  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-sm">
        <span className="font-medium">{label}</span>
        <span className="text-muted-foreground">{value}h</span>
      </div>
      <Progress value={(value / max) * 100} className="h-2" />
    </div>
  );
};

// Bullet Item Component
const BulletItem: React.FC<{
  text: string;
  variant?: "default" | "success";
}> = ({ text, variant = "default" }) => {
  return (
    <li className="flex items-start gap-3">
      <span
        className={`w-1.5 h-1.5 rounded-full mt-2 flex-shrink-0 ${
          variant === "success" ? "bg-success" : "bg-primary"
        }`}
      ></span>
      <span className="text-sm text-muted-foreground flex-1">{text}</span>
    </li>
  );
};

// Skill Row Component
const SkillRow: React.FC<{ skill: string; level: number }> = ({
  skill,
  level,
}) => {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-muted-foreground">{skill}</span>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((i) => (
          <div
            key={i}
            className={`w-2 h-2 rounded-full ${
              i <= level ? "bg-primary" : "bg-muted"
            }`}
          />
        ))}
      </div>
    </div>
  );
};

// Loading Skeleton Component
const LoadingSkeleton: React.FC<{ stage: number }> = ({ stage }) => {
  const stages = [
    "Analisando informações do projeto...",
    "Processando dados pessoais...",
    "Gerando insights...",
    "Finalizando resumo...",
  ];

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
            {stages[stage] || "Processando..."}
          </p>
          <div className="mt-4 max-w-md mx-auto h-2 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-500"
              style={{ width: `${((stage + 1) / stages.length) * 100}%` }}
            />
          </div>
        </div>

        <div className="space-y-4">
          <Card className="p-4 md:p-6">
            <Skeleton className="h-8 w-3/4 mb-4" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-2/3" />
          </Card>

          <Card className="p-4 md:p-6">
            <Skeleton className="h-6 w-1/2 mb-4" />
            <div className="space-y-3">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-12 w-full" />
            </div>
          </Card>

          <Card className="p-4 md:p-6">
            <div className="flex items-start gap-3 mb-4">
              <Skeleton className="w-12 h-12 md:w-14 md:h-14 rounded-full" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-5 w-20" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-3/4" />
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
