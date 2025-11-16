import { useState, useMemo, useCallback, useEffect } from "react";

export interface ProjectFormData {
  project_title: string;
  project_description: string;
  solution_proposal: string;
  problem_description: string;
  target_audience: string;
  value_proposition: string;
  customer_segment: string;
  revenue_model: string;
  competitive_advantage: string;
  innovation: string;
  social_impact: string;
  technical_feasibility: string;
  scalability: string;
  who_are_you: string;
  academy_info: string;
  market_info: string;
}

type ValidationRule = {
  key: keyof ProjectFormData;
  errorMessage: string;
  step: number;
};

const INITIAL_PROJECT_STATE: ProjectFormData = {
  project_title: "",
  project_description: "",
  solution_proposal: "",
  problem_description: "",
  target_audience: "",
  value_proposition: "",
  customer_segment: "",
  revenue_model: "",
  competitive_advantage: "",
  innovation: "",
  social_impact: "",
  technical_feasibility: "",
  scalability: "",
  who_are_you: "",
  academy_info: "",
  market_info: "",
};

const VALIDATION_RULES: ValidationRule[] = [
  {
    key: "project_title",
    errorMessage: "O título do projeto é obrigatório.",
    step: 1,
  },
  {
    key: "project_description",
    errorMessage: "A descrição é obrigatória.",
    step: 1,
  },
  {
    key: "solution_proposal",
    errorMessage: "A proposta de solução é obrigatória.",
    step: 1,
  },
  {
    key: "problem_description",
    errorMessage: "A descrição do problema é obrigatória.",
    step: 2,
  },
  {
    key: "target_audience",
    errorMessage: "O público-alvo é obrigatório.",
    step: 2,
  },
  {
    key: "value_proposition",
    errorMessage: "A proposta de valor é obrigatória.",
    step: 2,
  },
  {
    key: "customer_segment",
    errorMessage: "O segmento de clientes é obrigatório.",
    step: 3,
  },
  {
    key: "revenue_model",
    errorMessage: "O modelo de receita é obrigatório.",
    step: 3,
  },
  {
    key: "competitive_advantage",
    errorMessage: "A vantagem competitiva é obrigatória.",
    step: 3,
  },
  {
    key: "innovation",
    errorMessage: "O campo inovação é obrigatório.",
    step: 4,
  },
  {
    key: "social_impact",
    errorMessage: "O impacto social é obrigatório.",
    step: 4,
  },
  {
    key: "technical_feasibility",
    errorMessage: "A viabilidade técnica é obrigatória.",
    step: 4,
  },
  {
    key: "scalability",
    errorMessage: "A escalabilidade é obrigatória.",
    step: 4,
  },
  { key: "who_are_you", errorMessage: "Conte um pouco sobre você.", step: 5 },
  {
    key: "academy_info",
    errorMessage: "As informações acadêmicas são obrigatórias.",
    step: 5,
  },
  { key: "market_info", errorMessage: "O currículo é obrigatório.", step: 5 },
];

const STORAGE_KEY = "projectFormData";

const getMappedInitialData = (initialData?: any): ProjectFormData => {
  if (!initialData) {
    return INITIAL_PROJECT_STATE;
  }
  const mappedData = {
    ...INITIAL_PROJECT_STATE,
    ...initialData,
    problem_description: initialData.problem_description || "",
    innovation: initialData.innovation || "",
    social_impact: initialData.social_impact || "",
    technical_feasibility: initialData.technical_feasibility || "",
    revenue_model: initialData.revenue_model || "",
    scalability: initialData.scalability || "",
    customer_segment: initialData.customer_segment || "",
    competitive_advantage: initialData.competitive_advantage || "",
  };

  return mappedData;
};

export const useProjectForm = (totalSteps: number, initialData?: any) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<ProjectFormData>(() => {
    if (initialData) {
      return getMappedInitialData(initialData);
    }
    try {
      const savedData = localStorage.getItem(STORAGE_KEY);
      if (savedData) {
        const parsedData = JSON.parse(savedData);
        if (typeof parsedData === "object" && parsedData !== null) {
          return { ...INITIAL_PROJECT_STATE, ...parsedData };
        }
      }
    } catch (error) {
      console.error("Failed to parse localStorage data:", error);
      localStorage.removeItem(STORAGE_KEY);
    }
    return INITIAL_PROJECT_STATE;
  });
  const [errors, setErrors] = useState<
    Partial<Record<keyof ProjectFormData, string>>
  >({});

  useEffect(() => {
    if (initialData) {
      return;
    }
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
    } catch (error) {
      console.error("Failed to save to localStorage:", error);
    }
  }, [formData, initialData]);

  const handleInputChange = useCallback(
    (key: keyof ProjectFormData, value: string) => {
      setFormData((prev) => ({ ...prev, [key]: value }));
      setErrors((prev) => {
        if (value.trim()) {
          const newErrors = { ...prev };
          delete newErrors[key];
          return newErrors;
        }
        return prev;
      });
    },
    []
  );

  const validateStep = useCallback(() => {
    const currentRules = VALIDATION_RULES.filter((r) => r.step === currentStep);
    const newErrors = currentRules.reduce((acc, { key, errorMessage }) => {
      if (!formData[key]?.trim()) {
        acc[key] = errorMessage;
      }
      return acc;
    }, {} as Partial<Record<keyof ProjectFormData, string>>);

    setErrors((prev) => ({ ...prev, ...newErrors }));
    return Object.keys(newErrors).length === 0;
  }, [currentStep, formData]);

  const handleNext = useCallback(() => {
    if (validateStep() && currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [validateStep, currentStep, totalSteps]);

  const handlePrevious = useCallback(() => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [currentStep]);

  const FieldError = useCallback(
    ({ fieldKey }: { fieldKey: keyof ProjectFormData }) => (
      <div className="my-0.2">
        {errors[fieldKey] && (
          <span className="text-sm text-red-500">{errors[fieldKey]}</span>
        )}
      </div>
    ),
    [errors]
  );

  const getFieldProps = useCallback(
    (
      key: keyof ProjectFormData,
      placeholder: string,
      isTextArea: boolean = false,
      className?: string
    ) => ({
      value: formData[key],
      placeholder,
      className: `${errors[key] ? "ring-2 ring-red-500 border-red-500" : ""} ${
        isTextArea && className ? className : ""
      }`,
      onChange: (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
      ) => handleInputChange(key, e.target.value),
    }),
    [formData, errors, handleInputChange]
  );

  const stepTitles = useMemo(
    () => [
      {
        title: "Informações Básicas do Projeto",
        description:
          "Comece nos contando sobre o seu projeto: título, descrição e a solução que você propõe.",
      },
      {
        title: "Problema e Proposta de Valor",
        description:
          "Defina o problema que você está resolvendo, quem é seu público-alvo e qual valor você entrega.",
      },
      {
        title: "Modelo de Negócio (Lean Canvas)",
        description:
          "Descreva seu segmento de clientes, modelo de receita e vantagem competitiva.",
      },
      {
        title: "Inovação, Impacto e Viabilidade",
        description:
          "Conte sobre a inovação, o impacto social, a viabilidade técnica e o potencial de escalabilidade.",
      },
      {
        title: "Sobre Você",
        description:
          "Queremos conhecer você! Conte sobre sua trajetória, formação acadêmica e experiências.",
      },
    ],
    []
  );

  return {
    currentStep,
    formData,
    errors,
    handleNext,
    handlePrevious,
    validateStep,
    getFieldProps,
    FieldError,
    stepTitles,
  };
};

export const clearProjectFormData = () => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error(
      "Failed to clear project form data from localStorage:",
      error
    );
  }
};

export const hasSavedProjectFormData = (): boolean => {
  try {
    const saved = localStorage.getItem("projectFormData");
    if (!saved) return false;

    const parsed = JSON.parse(saved);
    if (!parsed || typeof parsed !== "object") return false;

    return Object.values(parsed).some(
      (value) => typeof value === "string" && value.trim() !== ""
    );
  } catch {
    return false;
  }
};