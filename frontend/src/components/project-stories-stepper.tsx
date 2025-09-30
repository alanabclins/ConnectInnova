"use client";

import React, { useState } from "react";
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
  const totalSteps = 3;

  const handleComplete = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });

    navigate("/summary", {
      state: {
        title: titleControlInput,
        description: projectDescriptionInput,
        solutionProposal: solutionProposalInput,
        socialImpact: socialImpactInput,
        technicalFeasibility: technicalFeasibilityInput,
        innovation: projectInnovationInput,
        whoAreYou: whoAreYouInput,
        academyInfo: academyInfo,
        marketInfo: marketInfo,
      },
    });

    if (onComplete) onComplete();
  };

  const handleNext = () => {
    if (currentStep < totalSteps) setCurrentStep(currentStep + 1);
  };

  const handlePrevious = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
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
        <form className="mb-4 h-full min-h-[300px] flex items-start">
          {currentStep === 1 && (
            <div className="flex flex-col md:flex-row gap-4 w-full">
              <div className="flex-1 flex flex-col">
                <Input
                  placeholder="Título do projeto"
                  className="mb-4"
                  value={titleControlInput}
                  onChange={(e) => setTitleControlInput(e.target.value)}
                />
                <Textarea
                  placeholder="Proposta de solução"
                  className="flex-1 min-h-[260px]"
                  value={solutionProposalInput}
                  onChange={(e) => setSolutionProposalInput(e.target.value)}
                />
              </div>

              <div className="flex-1">
                <Textarea
                  placeholder="Descrição do projeto"
                  className="w-full min-h-[260px]"
                  value={projectDescriptionInput}
                  onChange={(e) => setProjectDescriptionInput(e.target.value)}
                />
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="flex flex-col md:flex-row gap-4 w-full">
              <div className="flex-1 flex flex-col">
                <Textarea
                  placeholder="Impacto social"
                  className="mb-4 min-h-[100px]"
                  value={socialImpactInput}
                  onChange={(e) => setSocialImpactInput(e.target.value)}
                />
                <Textarea
                  placeholder="Viabilidade técnica"
                  className="flex-1 min-h-[200px]"
                  value={technicalFeasibilityInput}
                  onChange={(e) => setTechnicalFeasibilityInput(e.target.value)}
                />
              </div>

              <div className="flex-1">
                <Textarea
                  placeholder="Inovação"
                  className="w-full min-h-[260px]"
                  value={projectInnovationInput}
                  onChange={(e) => setProjectInnovationInput(e.target.value)}
                />
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="flex flex-col md:flex-row gap-4 w-full">
              <div className="flex-1">
                <Textarea
                  placeholder="Diga-nos quem é você."
                  className="w-full min-h-[280px]"
                  value={whoAreYouInput}
                  onChange={(e) => setWhoAreYouInput(e.target.value)}
                />
              </div>

              <div className="flex-1 flex flex-col">
                <Textarea
                  placeholder="Informações acadêmicas"
                  className="mb-4 min-h-[160px]"
                  value={academyInfo}
                  onChange={(e) => setAcademyInfo(e.target.value)}
                />
                <Textarea
                  placeholder="Currículo"
                  className="min-h-[140px]"
                  value={marketInfo}
                  onChange={(e) => setMarketInfo(e.target.value)}
                />
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
