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
import React, { type JSX } from "react";
import type { ProjectDetails } from "@/types/project.types";
import { Form } from "react-router-dom";

interface ProjectStepperProps {
  isEditing?: boolean;
  projectToEdit?: ProjectDetails;
  onComplete: (result: {
    projectId: string;
    projectData: { project_title: string; project_description: string };
  }) => void;
}

const TOTAL_STEPS = 5;

interface StepContentProps {
  getFieldProps: (
    key: keyof ProjectFormData,
    placeholder: string,
    isTextArea?: boolean,
    className?: string
  ) => any;
  FieldError: (props: { fieldKey: keyof ProjectFormData }) => JSX.Element;
}

const FormField: React.FC<{
  label: string;
  children: React.ReactNode;
  FieldError: JSX.Element;
  className?: string;
}> = ({ label, children, FieldError, className }) => (
  <div className={`flex flex-col gap-1.5 w-full ${className || ""}`}>
    <label className="text-sm font-medium text-muted-foreground">{label}</label>
    {children}
    <div className="min-h-5">{FieldError}</div>
  </div>
);

const Step1Content: React.FC<StepContentProps> = ({
  getFieldProps,
  FieldError,
}) => (
  <div className="flex flex-col md:flex-row gap-6 w-full flex-1">
    <div className="flex-1 flex flex-col gap-6">
      <FormField
        label="Título do projeto"
        FieldError={<FieldError fieldKey="project_title" />}
      >
        <Input {...getFieldProps("project_title", "Título do projeto")} />
      </FormField>

      <FormField
        label="Descrição do projeto"
        FieldError={<FieldError fieldKey="project_description" />}
        className="flex-1 flex flex-col"
      >
        <Textarea
          {...getFieldProps(
            "project_description",
            "Descreva de forma geral seu projeto",
            true,
            "flex-1"
          )}
        />
      </FormField>
    </div>
    <div className="flex-1 flex flex-col gap-6">
      <FormField
        label="Proposta de solução"
        FieldError={<FieldError fieldKey="solution_proposal" />}
        className="flex-1 flex flex-col"
      >
        <Textarea
          {...getFieldProps(
            "solution_proposal",
            "Como você pretende resolver o problema?",
            true,
            "flex-1"
          )}
        />
      </FormField>
    </div>
  </div>
);

const Step2Content: React.FC<StepContentProps> = ({
  getFieldProps,
  FieldError,
}) => (
  <div className="flex flex-col gap-6 w-full flex-1">
    <FormField
      label="Descrição do Problema"
      FieldError={<FieldError fieldKey="problem_description" />}
      className="flex-1 flex flex-col"
    >
      <Textarea
        {...getFieldProps(
          "problem_description",
          "Qual problema real você está resolvendo? Apresente dados, pesquisas ou evidências.",
          true,
          "flex-1"
        )}
      />
    </FormField>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <FormField
          label="Público-alvo"
          FieldError={<FieldError fieldKey="target_audience" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "target_audience",
              "Quem são os principais beneficiados? Descreva personas se possível.",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
      <div className="flex-1">
        <FormField
          label="Proposta de Valor"
          FieldError={<FieldError fieldKey="value_proposition" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "value_proposition",
              "Qual o principal benefício/diferencial que você oferece?",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
    </div>
  </div>
);

const Step3Content: React.FC<StepContentProps> = ({
  getFieldProps,
  FieldError,
}) => (
  <div className="flex flex-col gap-6 w-full flex-1">
    <FormField
      label="Segmento de Clientes"
      FieldError={<FieldError fieldKey="customer_segment" />}
      className="flex-1 flex flex-col"
    >
      <Textarea
        {...getFieldProps(
          "customer_segment",
          "Quem pagará pela solução? Defina perfil, tamanho do mercado.",
          true,
          "flex-1"
        )}
      />
    </FormField>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <FormField
          label="Modelo de Receita"
          FieldError={<FieldError fieldKey="revenue_model" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "revenue_model",
              "Como você vai ganhar dinheiro? Preços, planos, monetização.",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
      <div className="flex-1">
        <FormField
          label="Vantagem Competitiva"
          FieldError={<FieldError fieldKey="competitive_advantage" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "competitive_advantage",
              "O que torna sua solução difícil de copiar? Diferenciais únicos.",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
    </div>
  </div>
);

const Step4Content: React.FC<StepContentProps> = ({
  getFieldProps,
  FieldError,
}) => (
  <div className="flex flex-col gap-6 w-full flex-1">
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <FormField
          label="Grau de Inovação"
          FieldError={<FieldError fieldKey="innovation" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "innovation",
              "O que há de inovador? Tecnologias, métodos, abordagens únicas.",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
      <div className="flex-1">
        <FormField
          label="Impacto Social/Ambiental"
          FieldError={<FieldError fieldKey="social_impact" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "social_impact",
              "Quantas pessoas beneficiadas? Que mudança você gera?",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
    </div>
    <div className="flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <FormField
          label="Viabilidade Técnica e Econômica"
          FieldError={<FieldError fieldKey="technical_feasibility" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "technical_feasibility",
              "Tecnologias usadas, custos, recursos necessários.",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
      <div className="flex-1">
        <FormField
          label="Escalabilidade"
          FieldError={<FieldError fieldKey="scalability" />}
          className="h-full flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "scalability",
              "A solução pode crescer? Como replicar em outros contextos?",
              true,
              "flex-1"
            )}
          />
        </FormField>
      </div>
    </div>
  </div>
);

const Step5Content: React.FC<StepContentProps> = ({
  getFieldProps,
  FieldError,
}) => (
  <div className="flex flex-col md:flex-row gap-6 w-full flex-1">
    <div className="flex-1 flex flex-col gap-6">
      <FormField
        label="Quem é você?"
        FieldError={<FieldError fieldKey="who_are_you" />}
        className="flex-1 flex flex-col"
      >
        <Textarea
          {...getFieldProps(
            "who_are_you",
            "Conte sobre sua trajetória, experiências e motivações.",
            true,
            "flex-1"
          )}
        />
      </FormField>
    </div>
    <div className="flex-1 flex flex-col gap-6">
      <FormField
        label="Informações Acadêmicas"
        FieldError={<FieldError fieldKey="academy_info" />}
        className="flex-1 flex flex-col"
      >
        <Textarea
          {...getFieldProps(
            "academy_info",
            "Formação, instituição, curso, período.",
            true,
            "flex-1"
          )}
        />
      </FormField>
      <FormField
        label="Currículo/Experiência"
        FieldError={<FieldError fieldKey="market_info" />}
        className="flex-1 flex flex-col"
      >
        <Textarea
          {...getFieldProps(
            "market_info",
            "Projetos anteriores, habilidades, experiências relevantes.",
            true,
            "flex-1"
          )}
        />
      </FormField>
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
  isEditing,
  projectToEdit,
}) => {
  const {
    currentStep,
    formData,
    handleNext,
    handlePrevious,
    getFieldProps,
    FieldError: FieldErrorComponent,
    stepTitles,
    validateStep,
  } = useProjectForm(TOTAL_STEPS, projectToEdit);

  const CurrentStepComponent = STEP_COMPONENTS[currentStep];

  const handleCreateProject = async () => {
    try {
      const response = await ProjectService.createProject(formData);

      toast.success("Projeto adicionado com sucesso!", {
        description: "Iniciando análise de IA...",
      });

      onComplete({
        projectId: response.project_uuid,
        projectData: {
          project_title: formData.project_title,
          project_description: formData.project_description,
        },
      });
    } catch (error: any) {
      console.error("Erro ao criar projeto:", error);
      toast.error(
        "Não foi possível criar o projeto. Verifique sua conexão e tente novamente."
      );
    }
  };

  const handleUpdateProject = async () => {
    if (!projectToEdit?.uuid) {
      toast.error("ID do projeto não encontrado para atualização.");
      return;
    }

    try {
      await ProjectService.updateProject(projectToEdit.uuid, formData);
      toast.success("Projeto atualizado com sucesso!");

      onComplete({
        projectId: projectToEdit.uuid,
        projectData: {
          project_title: formData.project_title,
          project_description: formData.project_description,
        },
      });
    } catch (error: any) {
      console.error("Erro ao atualizar projeto:", error);
      toast.error("Não foi possível atualizar o projeto. Tente novamente.");
    }
  };

  const handleComplete = async () => {
    if (!validateStep()) return;
    window.scrollTo({ top: 0, behavior: "smooth" });

    if (isEditing) {
      await handleUpdateProject();
    } else {
      await handleCreateProject();
    }
  };

  const currentStepData = stepTitles[currentStep - 1];

  return (
    <div className="flex flex-col bg-background text-foreground">
      <div className="flex flex-col flex-grow w-full">
        <div className="flex justify-between items-start mb-8">
          <div className="max-w-2xl">
            <h1 className="text-2xl md:text-3xl font-bold mb-4">
              {isEditing
                ? `Editando: ${currentStepData.title}`
                : currentStepData.title}
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

        <div className="flex-grow flex flex-col justify-between">
          <Form className="mb-4 flex flex-col gap-6 w-full">
            {CurrentStepComponent && (
              <CurrentStepComponent
                getFieldProps={getFieldProps}
                FieldError={FieldErrorComponent}
              />
            )}
          </Form>

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
                <span>
                  {isEditing ? "Salvar Alterações" : "Tudo adicionado!"}
                </span>
                <IconCheck className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
