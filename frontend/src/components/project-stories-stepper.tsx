"use client";

import React, { useState } from "react";
import { CircularStepIndicator } from "./CircularStepIndicator";
import { FileUploadArea } from "./FileUploadArea";
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
  const [currentStep, setCurrentStep] = useState(1);
  const [formControl, setFormControl] = useState();
  const [isCompleted, setIsCompleted] = useState(false);
  const totalSteps = 3;

  const handleFilesSelected = (files: FileList) => {
    console.log(
      "Files selected:",
      Array.from(files).map((f) => f.name)
    );
  };

  const handleComplete = () => {
    setIsCompleted(true);
    if (onComplete) {
      onComplete();
    }
  };

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header with title and step indicator */}
        <div className="flex justify-between items-start mb-8">
          <div className="max-w-2xl">
            <h1 className="text-2xl md:text-4xl font-bold text-foreground mb-4">
              Tudo começa com o<br />
              seu projeto.
            </h1>
            <p className="text-muted-foreground text-md md:text-lg  leading-relaxed">
              Compartilhe tudo o que nos ajude a enxergar o seu projeto como
              você o vê.
              <br />
              Relatórios, documentos, imagens, links de repositório, guias de
              personas e o que mais fizer sentido.
            </p>
          </div>
          <CircularStepIndicator
            currentStep={currentStep}
            totalSteps={totalSteps}
          />
        </div>

        {/* Main content area */}
        <form action="submit" className="mb-8 h-80">
          {currentStep == 1 && (
            <div className="mb-8 flex-col md:flex-row flex gap-4">
              <div className="flex-1">
                <Input placeholder="Título do projeto" className="mb-4" />
                <Input placeholder="Descrição do " className="mb-4" />
                <Input placeholder="Descrição do " className="mb-4" />
                <Input placeholder="Descrição do " className="mb-4" />
                <Input placeholder="Descrição do " className="mb-4" />
              </div>

              <div className="flex-1">
                <Textarea placeholder="Descrição do projeto" />
              </div>
            </div>
          )}

          {currentStep == 2 && (
            <div className="mb-8 flex-col md:flex-row flex gap-4">
              <div className="flex-1">
                <Input placeholder="Título do projeto" className="mb-4" />
              </div>

              <div className="flex-1">
                <FileUploadArea onFilesSelected={handleFilesSelected} />
              </div>
            </div>
          )}
        </form>

        {/* Action buttons */}
        <div className="flex gap-4 mb-16 flex-wrap">
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

        {/* Footer with disclaimer and complete button */}
        <div className="flex flex-col md:flex-row justify-between items-start">
          <p className="text-muted-foreground text-sm max-w-md">
            Fique tranquilo: Suas informações são analisadas em total sigilo e
            nunca
            <br />
            serão compartilhadas sem seu consentimento explícito*
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
                className="bg-indigo-500 hover:bg-primary/90 text-primary-foreground px-6 gap-2"
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
