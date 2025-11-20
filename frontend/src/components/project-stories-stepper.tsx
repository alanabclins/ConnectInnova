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
import { clearProjectFormData, useProjectForm } from "@/hooks/useProjectForm";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import React, { type JSX, useMemo } from "react";
import type { ProjectDetails } from "@/types/project.types";

interface ProjectStepperProps {
  isEditing?: boolean;
  projectToEdit?: ProjectDetails;
  onComplete: (result: {
    projectId: string;
    projectData: { project_title: string; project_description: string };
  }) => void;
}

const TOTAL_STEPS = 5;

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

  const textareaSizing =
    "w-full min-h-[140px] max-h-[300px] lg:max-h-[35vh] overflow-auto resize-none break-all";

  const STEP_CONTENT = useMemo(
    () => [
      <div
        className="flex flex-col md:flex-row gap-6 w-full flex-1"
        key="step-1"
      >
        <div className="flex-1 flex flex-col gap-6">
          <FormField
            label="Título do projeto"
            FieldError={<FieldErrorComponent fieldKey="project_title" />}
          >
            <Input {...getFieldProps("project_title", "Título do projeto")} />
          </FormField>

          <FormField
            label="Descrição do projeto"
            FieldError={<FieldErrorComponent fieldKey="project_description" />}
            className="flex-1 flex flex-col"
          >
            <Textarea
              {...getFieldProps(
                "project_description",
                "Descreva de forma geral seu projeto",
                true,
                textareaSizing
              )}
            />
          </FormField>
        </div>
        <div className="flex-1 flex flex-col gap-6">
          <FormField
            label="Proposta de solução"
            FieldError={<FieldErrorComponent fieldKey="solution_proposal" />}
            className="flex-1 flex flex-col"
          >
            <Textarea
              {...getFieldProps(
                "solution_proposal",
                "Como você pretende resolver o problema?",
                true,
                textareaSizing
              )}
            />
          </FormField>
        </div>
      </div>,

      <div className="flex flex-col gap-6 w-full flex-1" key="step-2">
        <FormField
          label="Descrição do Problema"
          FieldError={<FieldErrorComponent fieldKey="problem_description" />}
          className="flex-1 flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "problem_description",
              "Qual problema real você está resolvendo? Apresente dados, pesquisas ou evidências.",
              true,
              textareaSizing
            )}
          />
        </FormField>
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex-1">
            <FormField
              label="Público-alvo"
              FieldError={<FieldErrorComponent fieldKey="target_audience" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "target_audience",
                  "Quem são os principais beneficiados? Descreva personas se possível.",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
          <div className="flex-1">
            <FormField
              label="Proposta de Valor"
              FieldError={<FieldErrorComponent fieldKey="value_proposition" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "value_proposition",
                  "Qual o principal benefício/diferencial que você oferece?",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
        </div>
      </div>,

      <div className="flex flex-col gap-6 w-full flex-1" key="step-3">
        <FormField
          label="Segmento de Clientes"
          FieldError={<FieldErrorComponent fieldKey="customer_segment" />}
          className="flex-1 flex flex-col"
        >
          <Textarea
            {...getFieldProps(
              "customer_segment",
              "Quem pagará pela solução? Defina perfil, tamanho do mercado.",
              true,
              textareaSizing
            )}
          />
        </FormField>
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex-1">
            <FormField
              label="Modelo de Receita"
              FieldError={<FieldErrorComponent fieldKey="revenue_model" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "revenue_model",
                  "Como você vai ganhar dinheiro? Preços, planos, monetização.",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
          <div className="flex-1">
            <FormField
              label="Vantagem Competitiva"
              FieldError={
                <FieldErrorComponent fieldKey="competitive_advantage" />
              }
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "competitive_advantage",
                  "O que torna sua solução difícil de copiar? Diferenciais únicos.",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
        </div>
      </div>,

      <div className="flex flex-col gap-6 w-full flex-1" key="step-4">
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex-1">
            <FormField
              label="Grau de Inovação"
              FieldError={<FieldErrorComponent fieldKey="innovation" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "innovation",
                  "O que há de inovador? Tecnologias, métodos, abordagens únicas.",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
          <div className="flex-1">
            <FormField
              label="Impacto Social/Ambiental"
              FieldError={<FieldErrorComponent fieldKey="social_impact" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "social_impact",
                  "Quantas pessoas beneficiadas? Que mudança você gera?",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
        </div>
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex-1">
            <FormField
              label="Viabilidade Técnica e Econômica"
              FieldError={
                <FieldErrorComponent fieldKey="technical_feasibility" />
              }
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "technical_feasibility",
                  "Tecnologias usadas, custos, recursos necessários.",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
          <div className="flex-1">
            <FormField
              label="Escalabilidade"
              FieldError={<FieldErrorComponent fieldKey="scalability" />}
              className="h-full flex flex-col"
            >
              <Textarea
                {...getFieldProps(
                  "scalability",
                  "A solução pode crescer? Como replicar em outros contextos?",
                  true,
                  textareaSizing
                )}
              />
            </FormField>
          </div>
        </div>
      </div>,

      <div
        className="flex flex-col md:flex-row gap-6 w-full flex-1"
        key="step-5"
      >
        <div className="flex-1 flex flex-col gap-6">
          <FormField
            label="Quem é você?"
            FieldError={<FieldErrorComponent fieldKey="who_are_you" />}
            className="flex-1 flex flex-col"
          >
            <Textarea
              {...getFieldProps(
                "who_are_you",
                "Conte sobre sua trajetória, experiências e motivações.",
                true,
                textareaSizing
              )}
            />
          </FormField>
        </div>
        <div className="flex-1 flex flex-col gap-6">
          <FormField
            label="Informações Acadêmicas"
            FieldError={<FieldErrorComponent fieldKey="academy_info" />}
            className="flex-1 flex flex-col"
          >
            <Textarea
              {...getFieldProps(
                "academy_info",
                "Formação, instituição, curso, período.",
                true,
                textareaSizing
              )}
            />
          </FormField>
          <FormField
            label="Currículo/Experiência"
            FieldError={<FieldErrorComponent fieldKey="market_info" />}
            className="flex-1 flex flex-col"
          >
            <Textarea
              {...getFieldProps(
                "market_info",
                "Projetos anteriores, habilidades, experiências relevantes.",
                true,
                textareaSizing
              )}
            />
          </FormField>
        </div>
      </div>,
    ],
    [getFieldProps, FieldErrorComponent]
  );

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

      clearProjectFormData();
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

    const apiPayload = {
      ...formData,
      clarity_problem: `Problema: ${formData.problem_description}\nPúblico-alvo: ${formData.target_audience}\nProposta de Valor: ${formData.value_proposition}`,
      inovation_grade: formData.innovation,
      social_impact_aggregated: formData.social_impact,
      tec_eco_viability: `Viabilidade Técnica: ${formData.technical_feasibility}\nModelo de Receita: ${formData.revenue_model}\nEscalabilidade: ${formData.scalability}`,
      application_potencial: `Segmento de Clientes: ${formData.customer_segment}\nVantagem Competitiva: ${formData.competitive_advantage}`,
    };

    try {
      await ProjectService.updateProject(projectToEdit.uuid, apiPayload);
      toast.success("Projeto atualizado com sucesso!");

      onComplete({
        projectId: projectToEdit.uuid,
        projectData: {
          project_title: formData.project_title,
          project_description: formData.project_description,
        },
      });

      clearProjectFormData();
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
          <form className="mb-4 flex flex-col gap-6 w-full flex-1">
            {STEP_CONTENT[currentStep - 1]}
          </form>

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
