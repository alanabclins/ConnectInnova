import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { AIGeneratedSummary } from "@/components/AiGeneratedSumary";

interface ProjectData {
  title: string;
  description: string;
  solutionProposal: string;
  socialImpact: string;
  technicalFeasibility: string;
  innovation: string;
  whoAreYou: string;
  academyInfo: string;
  marketInfo: string;
}

const defaultData: ProjectData = {
  title: "AgroPlus",
  description:
    "O objetivo é criar uma solução inteligente criada no ambiente acadêmico para tornar a gestão de propriedades rurais mais eficiente e acessível.",
  solutionProposal:
    "Solução trazendo sensores para o campo e dados claros do campo em tempo real para simplificar decisões...",
  socialImpact:
    "Auxiliar pequenos e médios produtores na melhora da gestão agrícola e aumento da produtividade de forma sustentável.",
  technicalFeasibility: "MVP desenvolvido com validação funcional concluída.",
  innovation:
    "Uso de IA para inferência de soluções e análise preditiva em tempo real.",
  whoAreYou:
    "Lucas, estudante de Ciências da Computação da UFPR e morador de Altamira-PA.",
  academyInfo: "Ciências da Computação - UFPR, 5º período",
  marketInfo:
    "Experiência em desenvolvimento de soluções web e mobile, com foco em projetos de impacto social.",
};

const SummaryPage = () => {
  const location = useLocation();
  const formData = location.state as Partial<ProjectData> | undefined;

  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  const projectData = { ...defaultData, ...formData };

  return <AIGeneratedSummary projectData={projectData} />;
};

export default SummaryPage;
