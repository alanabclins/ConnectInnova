"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProjectService from "@/services/project.service";
import { CircularStepIndicator } from "./CircularStepIndicator";
import { ActionButton } from "./ActionButton";
import { Button } from "@/components/ui/button";
import {
  IconBrandGithub,
  IconBrandYoutube,
  IconCheck,
  IconFileText,
} from "@tabler/icons-react";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";

interface ProjectStepperProps {
  onComplete?: () => void;
  // studentId: string; // Passa o studentId via props
}

type ValidationRule = {
  errorKey: string;
  inputValue: string;
  errorMessage: string;
};

export const ProjectStepper: React.FC<ProjectStepperProps> = ({
  onComplete,
  // studentId,
}) => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  
  // Passo 1: Informações Básicas
  const [titleControlInput, setTitleControlInput] = useState("");
  const [projectDescriptionInput, setProjectDescriptionInput] = useState("");
  const [solutionProposalInput, setSolutionProposalInput] = useState("");
  
  // Passo 2: Problema e Proposta de Valor
  const [problemDescriptionInput, setProblemDescriptionInput] = useState("");
  const [targetAudienceInput, setTargetAudienceInput] = useState("");
  const [valuePropositionInput, setValuePropositionInput] = useState("");
  
  // Passo 3: Modelo de Negócio (Lean Canvas)
  const [customerSegmentInput, setCustomerSegmentInput] = useState("");
  const [revenueModelInput, setRevenueModelInput] = useState("");
  const [competitiveAdvantageInput, setCompetitiveAdvantageInput] = useState("");
  
  // Passo 4: Inovação e Impacto
  const [projectInnovationInput, setProjectInnovationInput] = useState("");
  const [socialImpactInput, setSocialImpactInput] = useState("");
  const [technicalFeasibilityInput, setTechnicalFeasibilityInput] = useState("");
  const [scalabilityInput, setScalabilityInput] = useState("");
  
  // Passo 5: Informações Pessoais
  const [whoAreYouInput, setWhoAreYouInput] = useState("");
  const [academyInfo, setAcademyInfo] = useState("");
  const [marketInfo, setMarketInfo] = useState("");
  
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const totalSteps = 5;

  const handleInputChange = (
    key: string,
    value: string,
    setter: React.Dispatch<React.SetStateAction<string>>
  ) => {
    setter(value);
    setErrors((prev) => {
      const newErrors = { ...prev };
      if (value.trim()) delete newErrors[key];
      return newErrors;
    });
  };

  const handleComplete = async () => {
    if (!validateStep()) return;

    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      // Envia campos separados - agregação será feita no backend
      const projectData = {
        // Informações Básicas
        project_title: titleControlInput,
        project_description: projectDescriptionInput,
        solution_proposal: solutionProposalInput,
        
        // Problema e Proposta de Valor
        problem_description: problemDescriptionInput,
        target_audience: targetAudienceInput,
        value_proposition: valuePropositionInput,
        
        // Lean Canvas
        customer_segment: customerSegmentInput,
        revenue_model: revenueModelInput,
        competitive_advantage: competitiveAdvantageInput,
        
        // Inovação e Impacto
        innovation: projectInnovationInput,
        social_impact: socialImpactInput,
        technical_feasibility: technicalFeasibilityInput,
        scalability: scalabilityInput,
        
        // Informações Pessoais (Step 5)
        who_are_you: whoAreYouInput,
        academy_info: academyInfo,
        market_info: marketInfo,
      };

      const response = await ProjectService.createProject(projectData);
      console.log("Projeto criado com sucesso:", response);

      navigate("/home/summary", {
        state: {
          projectId: response.project_uuid,
          projectData: projectData
        },
      });

      if (onComplete) onComplete();
    } catch (error: any) {
      console.error("Erro ao criar projeto:", error);
      alert("Não foi possível criar o projeto. Tente novamente.");
    }
  };

  const handleNext = () => {
    if (validateStep() && currentStep < totalSteps)
      setCurrentStep(currentStep + 1);
  };

  const handlePrevious = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const FieldError = ({ message }: { message?: string }) => (
    <div className="my-0.2">
      {message && <span className="text-sm text-red-500">{message}</span>}
    </div>
  );

  const validationRulesByStep: Record<number, ValidationRule[]> = {
    1: [
      {
        errorKey: "title",
        inputValue: titleControlInput,
        errorMessage: "O título do projeto é obrigatório.",
      },
      {
        errorKey: "description",
        inputValue: projectDescriptionInput,
        errorMessage: "A descrição é obrigatória.",
      },
      {
        errorKey: "solution",
        inputValue: solutionProposalInput,
        errorMessage: "A proposta de solução é obrigatória.",
      },
    ],
    2: [
      {
        errorKey: "problem",
        inputValue: problemDescriptionInput,
        errorMessage: "A descrição do problema é obrigatória.",
      },
      {
        errorKey: "target",
        inputValue: targetAudienceInput,
        errorMessage: "O público-alvo é obrigatório.",
      },
      {
        errorKey: "value",
        inputValue: valuePropositionInput,
        errorMessage: "A proposta de valor é obrigatória.",
      },
    ],
    3: [
      {
        errorKey: "segment",
        inputValue: customerSegmentInput,
        errorMessage: "O segmento de clientes é obrigatório.",
      },
      {
        errorKey: "revenue",
        inputValue: revenueModelInput,
        errorMessage: "O modelo de receita é obrigatório.",
      },
      {
        errorKey: "advantage",
        inputValue: competitiveAdvantageInput,
        errorMessage: "A vantagem competitiva é obrigatória.",
      },
    ],
    4: [
      {
        errorKey: "innovation",
        inputValue: projectInnovationInput,
        errorMessage: "O campo inovação é obrigatório.",
      },
      {
        errorKey: "social",
        inputValue: socialImpactInput,
        errorMessage: "O impacto social é obrigatório.",
      },
      {
        errorKey: "technical",
        inputValue: technicalFeasibilityInput,
        errorMessage: "A viabilidade técnica é obrigatória.",
      },
      {
        errorKey: "scalability",
        inputValue: scalabilityInput,
        errorMessage: "A escalabilidade é obrigatória.",
      },
    ],
    5: [
      {
        errorKey: "who",
        inputValue: whoAreYouInput,
        errorMessage: "Conte um pouco sobre você.",
      },
      {
        errorKey: "academy",
        inputValue: academyInfo,
        errorMessage: "As informações acadêmicas são obrigatórias.",
      },
      {
        errorKey: "market",
        inputValue: marketInfo,
        errorMessage: "O currículo é obrigatório.",
      },
    ],
  };

  const validateStep = () => {
    const currentRules = validationRulesByStep[currentStep] || [];
    const newErrors = currentRules.reduce(
      (acc, { errorKey, inputValue, errorMessage }) => {
        if (!inputValue?.trim()) acc[errorKey] = errorMessage;
        return acc;
      },
      {} as Record<string, string>
    );

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-8">
          <div className="max-w-2xl">
            {currentStep === 1 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Informações Básicas do Projeto
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Comece nos contando sobre o seu projeto: título, descrição e a solução que você propõe.
                </p>
              </>
            )}
            {currentStep === 2 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Problema e Proposta de Valor
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Defina o problema que você está resolvendo, quem é seu público-alvo e qual valor você entrega.
                </p>
              </>
            )}
            {currentStep === 3 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Modelo de Negócio (Lean Canvas)
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Descreva seu segmento de clientes, modelo de receita e vantagem competitiva.
                </p>
              </>
            )}
            {currentStep === 4 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Inovação, Impacto e Viabilidade
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Conte sobre a inovação, o impacto social, a viabilidade técnica e o potencial de escalabilidade.
                </p>
              </>
            )}
            {currentStep === 5 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Sobre Você
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Queremos conhecer você! Conte sobre sua trajetória, formação acadêmica e experiências.
                </p>
              </>
            )}
          </div>
          <CircularStepIndicator
            currentStep={currentStep}
            totalSteps={totalSteps}
          />
        </div>

        {/* Step content */}
        <form className="mb-4 min-h-[320px] flex flex-col gap-6 w-full">
          {/* Passo 1: Informações Básicas */}
          {currentStep === 1 && (
            <div className="flex flex-col md:flex-row gap-6 w-full">
              <div className="flex-1 flex flex-col gap-3">
                <Input
                  placeholder="Título do projeto"
                  value={titleControlInput}
                  className={errors.title ? "ring-2 ring-red-500 border-red-500" : ""}
                  onChange={(e) =>
                    handleInputChange("title", e.target.value, setTitleControlInput)
                  }
                />
                <FieldError message={errors.title} />

                <Textarea
                  placeholder="Descrição do projeto - Descreva de forma geral seu projeto"
                  className={`min-h-[260px] ${
                    errors.description ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={projectDescriptionInput}
                  onChange={(e) =>
                    handleInputChange("description", e.target.value, setProjectDescriptionInput)
                  }
                />
                <FieldError message={errors.description} />
              </div>

              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Proposta de solução - Como você pretende resolver o problema?"
                  className={`min-h-[340px] ${
                    errors.solution ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={solutionProposalInput}
                  onChange={(e) =>
                    handleInputChange("solution", e.target.value, setSolutionProposalInput)
                  }
                />
                <FieldError message={errors.solution} />
              </div>
            </div>
          )}

          {/* Passo 2: Problema e Proposta de Valor */}
          {currentStep === 2 && (
            <div className="flex flex-col gap-6 w-full">
              <div className="flex flex-col gap-3">
                <Textarea
                  placeholder="Descrição do Problema - Qual problema real você está resolvendo? Apresente dados, pesquisas ou evidências."
                  className={`min-h-[140px] ${
                    errors.problem ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={problemDescriptionInput}
                  onChange={(e) =>
                    handleInputChange("problem", e.target.value, setProblemDescriptionInput)
                  }
                />
                <FieldError message={errors.problem} />
              </div>

              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Público-alvo - Quem são os principais beneficiados? Descreva personas se possível."
                    className={`min-h-[140px] ${
                      errors.target ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={targetAudienceInput}
                    onChange={(e) =>
                      handleInputChange("target", e.target.value, setTargetAudienceInput)
                    }
                  />
                  <FieldError message={errors.target} />
                </div>

                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Proposta de Valor - Qual o principal benefício/diferencial que você oferece?"
                    className={`min-h-[140px] ${
                      errors.value ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={valuePropositionInput}
                    onChange={(e) =>
                      handleInputChange("value", e.target.value, setValuePropositionInput)
                    }
                  />
                  <FieldError message={errors.value} />
                </div>
              </div>
            </div>
          )}

          {/* Passo 3: Modelo de Negócio (Lean Canvas) */}
          {currentStep === 3 && (
            <div className="flex flex-col gap-6 w-full">
              <div className="flex flex-col gap-3">
                <Textarea
                  placeholder="Segmento de Clientes - Quem pagará pela solução? Defina perfil, tamanho do mercado."
                  className={`min-h-[120px] ${
                    errors.segment ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={customerSegmentInput}
                  onChange={(e) =>
                    handleInputChange("segment", e.target.value, setCustomerSegmentInput)
                  }
                />
                <FieldError message={errors.segment} />
              </div>

              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Modelo de Receita - Como você vai ganhar dinheiro? Preços, planos, monetização."
                    className={`min-h-[140px] ${
                      errors.revenue ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={revenueModelInput}
                    onChange={(e) =>
                      handleInputChange("revenue", e.target.value, setRevenueModelInput)
                    }
                  />
                  <FieldError message={errors.revenue} />
                </div>

                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Vantagem Competitiva - O que torna sua solução difícil de copiar? Diferenciais únicos."
                    className={`min-h-[140px] ${
                      errors.advantage ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={competitiveAdvantageInput}
                    onChange={(e) =>
                      handleInputChange("advantage", e.target.value, setCompetitiveAdvantageInput)
                    }
                  />
                  <FieldError message={errors.advantage} />
                </div>
              </div>
            </div>
          )}

          {/* Passo 4: Inovação e Impacto */}
          {currentStep === 4 && (
            <div className="flex flex-col gap-6 w-full">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Grau de Inovação - O que há de inovador? Tecnologias, métodos, abordagens únicas."
                    className={`min-h-[150px] ${
                      errors.innovation ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={projectInnovationInput}
                    onChange={(e) =>
                      handleInputChange("innovation", e.target.value, setProjectInnovationInput)
                    }
                  />
                  <FieldError message={errors.innovation} />
                </div>

                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Impacto Social/Ambiental - Quantas pessoas beneficiadas? Que mudança você gera?"
                    className={`min-h-[150px] ${
                      errors.social ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={socialImpactInput}
                    onChange={(e) =>
                      handleInputChange("social", e.target.value, setSocialImpactInput)
                    }
                  />
                  <FieldError message={errors.social} />
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Viabilidade Técnica e Econômica - Tecnologias usadas, custos, recursos necessários."
                    className={`min-h-[120px] ${
                      errors.technical ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={technicalFeasibilityInput}
                    onChange={(e) =>
                      handleInputChange("technical", e.target.value, setTechnicalFeasibilityInput)
                    }
                  />
                  <FieldError message={errors.technical} />
                </div>

                <div className="flex-1 flex flex-col gap-3">
                  <Textarea
                    placeholder="Escalabilidade - A solução pode crescer? Como replicar em outros contextos?"
                    className={`min-h-[120px] ${
                      errors.scalability ? "ring-2 ring-red-500 border-red-500" : ""
                    }`}
                    value={scalabilityInput}
                    onChange={(e) =>
                      handleInputChange("scalability", e.target.value, setScalabilityInput)
                    }
                  />
                  <FieldError message={errors.scalability} />
                </div>
              </div>
            </div>
          )}

          {/* Passo 5: Informações Pessoais */}
          {currentStep === 5 && (
            <div className="flex flex-col md:flex-row gap-6 w-full">
              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Quem é você? - Conte sobre sua trajetória, experiências e motivações."
                  className={`min-h-[200px] ${
                    errors.who ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={whoAreYouInput}
                  onChange={(e) =>
                    handleInputChange("who", e.target.value, setWhoAreYouInput)
                  }
                />
                <FieldError message={errors.who} />
              </div>

              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Informações Acadêmicas - Formação, instituição, curso, período."
                  className={`min-h-[100px] ${
                    errors.academy ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={academyInfo}
                  onChange={(e) =>
                    handleInputChange("academy", e.target.value, setAcademyInfo)
                  }
                />
                <FieldError message={errors.academy} />
                <Textarea
                  placeholder="Currículo/Experiência - Projetos anteriores, habilidades, experiências relevantes."
                  className={`min-h-[100px] ${
                    errors.market ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={marketInfo}
                  onChange={(e) =>
                    handleInputChange("market", e.target.value, setMarketInfo)
                  }
                />
                <FieldError message={errors.market} />
              </div>
            </div>
          )}
        </form>

        {/* Action buttons */}
        <div className="flex flex-wrap gap-4 mb-8">
          <ActionButton
            icon={IconFileText}
            label="Links para documentos"
            onClick={() => console.log("Documents clicked")}
          />
          <ActionButton
            icon={IconBrandYoutube}
            label="Link do Youtube"
            onClick={() => console.log("YouTube clicked")}
          />
          <ActionButton
            icon={IconBrandGithub}
            label="Repositório Github"
            onClick={() => console.log("GitHub clicked")}
          />
        </div>

        {/* Footer */}
        <div className="flex flex-col md:flex-row justify-between items-start">
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
            {currentStep < totalSteps && (
              <Button onClick={handleNext} className="px-6">
                Próximo
              </Button>
            )}
            {currentStep === totalSteps && (
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
