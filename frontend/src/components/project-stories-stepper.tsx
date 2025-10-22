import { useNavigate } from "react-router-dom";
import ProjectService from "@/services/project.service";
import { CircularStepIndicator } from "./CircularStepIndicator";
import { ActionButton } from "./ActionButton";
import { Button } from "./ui/button";
import {
  IconBrandGithub,
  IconBrandYoutube,
  IconCheck,
  IconFileText,
} from "@tabler/icons-react";
import { toast } from "sonner";
import { useProjectForm, type ProjectFormData } from "@/hooks/useProjectForm";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import type { JSX } from "react";

interface ProjectStepperProps {
  onComplete?: () => void;
}

const TOTAL_STEPS = 5;

interface StepContentProps {
  getFieldProps: (key: keyof ProjectFormData, placeholder: string, isTextArea?: boolean, minHeightClass?: string) => any;
  FieldError: (props: { fieldKey: keyof ProjectFormData }) => JSX.Element;
}

const Step1Content: React.FC<StepContentProps> = ({ getFieldProps, FieldError }) => (
  <div className="flex flex-col md:flex-row gap-6 w-full">
    <div className="flex-1 flex flex-col gap-3">
      <Input {...getFieldProps("project_title", "Título do projeto")} />
      <FieldError fieldKey="project_title" />

      <Textarea
        {...getFieldProps("project_description", "Descrição do projeto - Descreva de forma geral seu projeto", true, "min-h-[260px]")}
      />
      <FieldError fieldKey="project_description" />
    </div>
    <div className="flex-1 flex flex-col gap-4">
      <Textarea
        {...getFieldProps("solution_proposal", "Proposta de solução - Como você pretende resolver o problema?", true, "min-h-[340px]")}
      />
      <FieldError fieldKey="solution_proposal" />
    </div>
  </div>
);

const Step2Content: React.FC<StepContentProps> = ({ getFieldProps, FieldError }) => (
  <div className="flex flex-col gap-6 w-full">
    <div className="flex flex-col gap-3">
      <Textarea
        {...getFieldProps("problem_description", "Descrição do Problema - Qual problema real você está resolvendo? Apresente dados, pesquisas ou evidências.", true, "min-h-[140px]")}
      />
      <FieldError fieldKey="problem_description" />
    </div>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("target_audience", "Público-alvo - Quem são os principais beneficiados? Descreva personas se possível.", true, "min-h-[140px]")}
        />
        <FieldError fieldKey="target_audience" />
      </div>
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("value_proposition", "Proposta de Valor - Qual o principal benefício/diferencial que você oferece?", true, "min-h-[140px]")}
        />
        <FieldError fieldKey="value_proposition" />
      </div>
    </div>
  </div>
);

const Step3Content: React.FC<StepContentProps> = ({ getFieldProps, FieldError }) => (
  <div className="flex flex-col gap-6 w-full">
    <div className="flex flex-col gap-3">
      <Textarea
        {...getFieldProps("customer_segment", "Segmento de Clientes - Quem pagará pela solução? Defina perfil, tamanho do mercado.", true, "min-h-[120px]")}
      />
      <FieldError fieldKey="customer_segment" />
    </div>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("revenue_model", "Modelo de Receita - Como você vai ganhar dinheiro? Preços, planos, monetização.", true, "min-h-[140px]")}
        />
        <FieldError fieldKey="revenue_model" />
      </div>
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("competitive_advantage", "Vantagem Competitiva - O que torna sua solução difícil de copiar? Diferenciais únicos.", true, "min-h-[140px]")}
        />
        <FieldError fieldKey="competitive_advantage" />
      </div>
    </div>
  </div>
);

const Step4Content: React.FC<StepContentProps> = ({ getFieldProps, FieldError }) => (
  <div className="flex flex-col gap-6 w-full">
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("innovation", "Grau de Inovação - O que há de inovador? Tecnologias, métodos, abordagens únicas.", true, "min-h-[150px]")}
        />
        <FieldError fieldKey="innovation" />
      </div>
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("social_impact", "Impacto Social/Ambiental - Quantas pessoas beneficiadas? Que mudança você gera?", true, "min-h-[150px]")}
        />
        <FieldError fieldKey="social_impact" />
      </div>
    </div>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("technical_feasibility", "Viabilidade Técnica e Econômica - Tecnologias usadas, custos, recursos necessários.", true, "min-h-[120px]")}
        />
        <FieldError fieldKey="technical_feasibility" />
      </div>
      <div className="flex-1 flex flex-col gap-3">
        <Textarea
          {...getFieldProps("scalability", "Escalabilidade - A solução pode crescer? Como replicar em outros contextos?", true, "min-h-[120px]")}
        />
        <FieldError fieldKey="scalability" />
      </div>
    </div>
  </div>
);

const Step5Content: React.FC<StepContentProps> = ({ getFieldProps, FieldError }) => (
  <div className="flex flex-col md:flex-row gap-6 w-full">
    <div className="flex-1 flex flex-col gap-4">
      <Textarea
        {...getFieldProps("who_are_you", "Quem é você? - Conte sobre sua trajetória, experiências e motivações.", true, "min-h-[200px]")}
      />
      <FieldError fieldKey="who_are_you" />
    </div>
    <div className="flex-1 flex flex-col gap-4">
      <Textarea
        {...getFieldProps("academy_info", "Informações Acadêmicas - Formação, instituição, curso, período.", true, "min-h-[100px]")}
      />
      <FieldError fieldKey="academy_info" />
      <Textarea
        {...getFieldProps("market_info", "Currículo/Experiência - Projetos anteriores, habilidades, experiências relevantes.", true, "min-h-[100px]")}
      />
      <FieldError fieldKey="market_info" />
    </div>
  </div>
);

const STEP_COMPONENTS: Record<number, React.FC<StepContentProps>> = {
  1: Step1Content,
  2: Step2Content,
  3: Step3Content,
  4: Step4Content,
  5: Step5Content,
};

export const ProjectStepper: React.FC<ProjectStepperProps> = ({
  onComplete,
}) => {
  const navigate = useNavigate();
  const {
    currentStep,
    formData,
    handleNext,
    handlePrevious,
    getFieldProps,
    FieldError: FieldErrorComponent,
    stepTitles,
    validateStep,
  } = useProjectForm(TOTAL_STEPS);

  const CurrentStepComponent = STEP_COMPONENTS[currentStep];

  const handleComplete = async () => {
    if (!validateStep()) return;

    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      const response = await ProjectService.createProject(formData);
      
      toast.success("Projeto adicionado com sucesso!", {
        description: "Iniciando análise de IA...",
      });

      navigate("/home/summary", {
        state: {
          projectId: response.project_uuid,
          projectData: {
            project_title: formData.project_title,
            project_description: formData.project_description,
          },
        },
      });

      if (onComplete) onComplete();
    } catch (error: any) {
      console.error("Erro ao criar projeto:", error);
      toast.error(
        "Não foi possível criar o projeto. Verifique sua conexão e tente novamente."
      );
    }
  };

  const currentStepData = stepTitles[currentStep - 1];

  return (
    <div className="min-h-[calc(100dvh-80px)] flex flex-col bg-background text-foreground px-8 py-12">
      <div className="max-w-7xl mx-auto flex flex-col flex-grow w-full">
        {/* Header */}
        <div className="flex justify-between items-start mb-8">
          <div className="max-w-2xl">
            <h1 className="text-2xl md:text-3xl font-bold mb-4">
              {currentStepData.title}
            </h1>
            <p className="text-muted-foreground text-md md:text-md leading-relaxed">
              {currentStepData.description}
            </p>
          </div>
          <CircularStepIndicator
            currentStep={currentStep}
            totalSteps={TOTAL_STEPS}
          />
        </div>

        {/* Step content and Action buttons (Conteúdo principal) */}
        <div className="flex-grow flex flex-col justify-between">
          <form className="mb-4 flex flex-col gap-6 w-full">
            {CurrentStepComponent && (
              <CurrentStepComponent 
                getFieldProps={getFieldProps} 
                FieldError={FieldErrorComponent} 
              />
            )}
          </form>

          {/* Action buttons - Movidos para dentro do flex-grow, mas acima do footer */}
          <div className="flex flex-wrap gap-4 mt-auto mb-8">
            <ActionButton
              icon={IconFileText}
              label="Links para documentos"
              onClick={() => toast.info("Funcionalidade em desenvolvimento.")}
            />
            <ActionButton
              icon={IconBrandYoutube}
              label="Link do Youtube"
              onClick={() => toast.info("Funcionalidade em desenvolvimento.")}
            />
            <ActionButton
              icon={IconBrandGithub}
              label="Repositório Github"
              onClick={() => toast.info("Funcionalidade em desenvolvimento.")}
            />
          </div>
        </div>


        {/* Footer */}
        <div className="flex flex-col md:flex-row justify-between items-start pt-8 md:pt-0">
          <p className="text-muted-foreground text-sm max-w-md">
            Fique tranquilo: Suas informações são analisadas em total sigilo e
            nunca serão compartilhadas sem seu consentimento explícito*
          </p>

          <div className="py-8 md:py-0 flex gap-4 items-center">
            {currentStep > 1 && (
              <Button
                variant="secondary"
                onClick={handlePrevious}
                className="px-6"
              >
                Anterior
              </Button>
            )}
            {currentStep < TOTAL_STEPS && (
              <Button onClick={handleNext} className="px-6">
                Próximo
              </Button>
            )}
            {currentStep === TOTAL_STEPS && (
              <Button
                onClick={handleComplete}
                className="bg-primary hover:bg-primary/90 text-primary-foreground px-6 gap-2"
              >
                <span>Tudo adicionado!</span>
                <IconCheck className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};