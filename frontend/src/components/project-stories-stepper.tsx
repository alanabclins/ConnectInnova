"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
}

type ValidationRule = {
  errorKey: string;
  inputValue: string;
  errorMessage: string;
};

export const ProjectStepper: React.FC<ProjectStepperProps> = ({
  onComplete,
}) => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [titleControlInput, setTitleControlInput] = useState("");
  const [projectDescriptionInput, setProjectDescriptionInput] = useState("");
  const [solutionProposalInput, setSolutionProposalInput] = useState("");
  const [socialImpactInput, setSocialImpactInput] = useState("");
  const [technicalFeasibilityInput, setTechnicalFeasibilityInput] =
    useState("");
  const [projectInnovationInput, setProjectInnovationInput] = useState("");
  const [whoAreYouInput, setWhoAreYouInput] = useState("");
  const [academyInfo, setAcademyInfo] = useState("");
  const [marketInfo, setMarketInfo] = useState("");
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const totalSteps = 3;

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

  const handleComplete = () => {
    if (validateStep()) {
      window.scrollTo({ top: 0, behavior: "smooth" });

      navigate("/home/summary", {
        // state: {
        //   title: titleControlInput,
        //   description: projectDescriptionInput,
        //   solutionProposal: solutionProposalInput,
        //   socialImpact: socialImpactInput,
        //   technicalFeasibility: technicalFeasibilityInput,
        //   innovation: projectInnovationInput,
        //   whoAreYou: whoAreYouInput,
        //   academyInfo: academyInfo,
        //   marketInfo: marketInfo,
        // },
      });
    }

    if (onComplete) onComplete();
  };

  const handleNext = () => {
    if (validateStep()) {
      if (currentStep < totalSteps) setCurrentStep(currentStep + 1);
    }
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
        errorKey: "solution",
        inputValue: solutionProposalInput,
        errorMessage: "A proposta de solução é obrigatória.",
      },
      {
        errorKey: "description",
        inputValue: projectDescriptionInput,
        errorMessage: "A descrição é obrigatória.",
      },
    ],
    2: [
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
        errorKey: "innovation",
        inputValue: projectInnovationInput,
        errorMessage: "O campo inovação é obrigatório.",
      },
    ],
    3: [
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
      (errors, { errorKey, inputValue, errorMessage }) => {
        if (!inputValue?.trim()) errors[errorKey] = errorMessage;
        return errors;
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
            {currentStep <= 2 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Tudo começa com o seu projeto.
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Compartilhe tudo o que nos ajude a enxergar o seu projeto como
                  você o vê. Relatórios, documentos, imagens, links de
                  repositório, guias de personas e o que mais fizer sentido.
                </p>
              </>
            )}
            {currentStep === 3 && (
              <>
                <h1 className="text-2xl md:text-3xl font-bold mb-4">
                  Deixe a gente conhecer você melhor.
                </h1>
                <p className="text-muted-foreground text-md md:text-md leading-relaxed">
                  Quem é você por trás do projeto? Conte sobre sua trajetória,
                  experiências, pontos fortes, desafios sociais ou pessoais.
                  Queremos entender um pouco da sua história.
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
          {currentStep === 1 && (
            <div className="flex flex-col md:flex-row gap-6 w-full">
              <div className="flex-1 flex flex-col gap-3">
                <Input
                  placeholder="Título do projeto"
                  value={titleControlInput}
                  className={`${
                    errors.title ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  onChange={(e) =>
                    handleInputChange(
                      "title",
                      e.target.value,
                      setTitleControlInput
                    )
                  }
                />
                <FieldError message={errors.title} />

                <Textarea
                  placeholder="Proposta de solução"
                  className={`min-h-[260px] ${
                    errors.solution ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={solutionProposalInput}
                  onChange={(e) =>
                    handleInputChange(
                      "solution",
                      e.target.value,
                      setSolutionProposalInput
                    )
                  }
                />
                <FieldError message={errors.solution} />
              </div>

              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Descrição do projeto"
                  className={`min-h-[260px] ${
                    errors.description
                      ? "ring-2 ring-red-500 border-red-500"
                      : ""
                  }`}
                  value={projectDescriptionInput}
                  onChange={(e) =>
                    handleInputChange(
                      "description",
                      e.target.value,
                      setProjectDescriptionInput
                    )
                  }
                />
                <FieldError message={errors.description} />
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="flex flex-col md:flex-row gap-6 w-full">
              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Impacto social"
                  className={`min-h-[196px] ${
                    errors.social ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={socialImpactInput}
                  onChange={(e) =>
                    handleInputChange(
                      "social",
                      e.target.value,
                      setSocialImpactInput
                    )
                  }
                />
                <FieldError message={errors.social} />
                <Textarea
                  placeholder="Viabilidade técnica"
                  className={`min-h-[100px] ${
                    errors.technical ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={technicalFeasibilityInput}
                  onChange={(e) =>
                    handleInputChange(
                      "technical",
                      e.target.value,
                      setTechnicalFeasibilityInput
                    )
                  }
                />
                <FieldError message={errors.technical} />
              </div>

              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Inovação"
                  className={`min-h-[260px] ${
                    errors.innovation
                      ? "ring-2 ring-red-500 border-red-500"
                      : ""
                  }`}
                  value={projectInnovationInput}
                  onChange={(e) =>
                    handleInputChange(
                      "innovation",
                      e.target.value,
                      setProjectInnovationInput
                    )
                  }
                />
                <FieldError message={errors.innovation} />
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="flex flex-col md:flex-row gap-6 w-full">
              <div className="flex-1 flex flex-col gap-4">
                <Textarea
                  placeholder="Diga-nos quem é você."
                  className={`min-h-[280px] ${
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
                  placeholder="Informações acadêmicas"
                  className={`min-h-[160px] ${
                    errors.academy ? "ring-2 ring-red-500 border-red-500" : ""
                  }`}
                  value={academyInfo}
                  onChange={(e) =>
                    handleInputChange("academy", e.target.value, setAcademyInfo)
                  }
                />
                <FieldError message={errors.academy} />
                <Textarea
                  placeholder="Currículo"
                  className={`min-h-[140px] ${
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
