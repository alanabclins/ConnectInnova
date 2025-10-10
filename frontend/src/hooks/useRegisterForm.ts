import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { z, ZodError } from "zod";
import { toast } from "sonner";
import authService from "@/services/auth.service";

// Validação da senha movida para uma constante para reutilização e clareza.
const passwordValidation = z
  .string()
  .min(8, "A senha deve ter no mínimo 8 caracteres")
  .regex(/[A-Z]/, "A senha deve conter uma letra maiúscula")
  .regex(/[a-z]/, "A senha deve conter uma letra minúscula")
  .regex(/[0-9]/, "A senha deve conter um número")
  .regex(/[^A-Za-z0-9]/, "A senha deve conter um caractere especial");

// Schema de validação completo com a confirmação de senha.
const registerSchema = z
  .object({
    fullName: z.string().min(3, "O nome deve ter no mínimo 3 caracteres"),
    email: z.string().email("Email inválido").min(1, "Email é obrigatório"),
    password: passwordValidation,
    confirmPassword: z.string(), // Campo para a confirmação
  })
  // Validação para garantir que as senhas coincidem.
  .refine((data) => data.password === data.confirmPassword, {
    message: "As senhas não coincidem",
    path: ["confirmPassword"], // O erro será exibido no campo de confirmação.
  });

export const useRegisterForm = () => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [submitErrors, setSubmitErrors] = useState<{
    fullName?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});
  const [inlineEmailError, setInlineEmailError] = useState<string | null>(null);
  const [showPasswordRequirements, setShowPasswordRequirements] =
    useState(false);
  const [passwordChecks, setPasswordChecks] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    specialChar: false,
  });
  const navigate = useNavigate();

  useEffect(() => {
    setPasswordChecks({
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      specialChar: /[^A-Za-z0-9]/.test(password),
    });
  }, [password]);

  const handleEmailBlur = () => {
    if (!email) {
      setInlineEmailError(null);
      return;
    }
    try {
      z.string().email("Formato de email inválido").parse(email);
      setInlineEmailError(null);
    } catch (error) {
      if (error instanceof ZodError) {
        setInlineEmailError(error.issues[0].message);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitErrors({});
    setIsLoading(true);

    try {
      registerSchema.parse({ fullName, email, password, confirmPassword });
      const userData = { email, password, full_name: fullName };
      await authService.register(userData);
      toast.success("Cadastro realizado com sucesso!", {
        description: "Você será redirecionado para a página de login.",
      });
      setTimeout(() => navigate("/"), 1500);
    } catch (error) {
      if (error instanceof ZodError) {
        const fieldErrors: {
          fullName?: string;
          email?: string;
          password?: string;
          confirmPassword?: string;
        } = {};
        error.issues.forEach((issue) => {
          const field = issue.path[0] as keyof typeof fieldErrors;
          fieldErrors[field] = issue.message;
        });
        setSubmitErrors(fieldErrors);
        toast.error("Erro de validação", {
          description: "Por favor, corrija os campos indicados.",
        });
      } else if ((error as any)?.response?.status === 409) {
        toast.error("Erro ao cadastrar", {
          description: "Este email já está em uso.",
        });
        setSubmitErrors({ email: "Este email já está em uso." });
      } else {
        toast.error("Erro ao cadastrar", {
          description:
            (error as any)?.response?.data?.detail ||
            "Tente novamente mais tarde",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    models: {
      fullName,
      email,
      password,
      confirmPassword,
      showPassword,
      isLoading,
      submitErrors,
      inlineEmailError,
      showPasswordRequirements,
      passwordChecks,
    },
    handlers: {
      setFullName,
      setEmail,
      setPassword,
      setConfirmPassword,
      setShowPassword,
      setShowPasswordRequirements,
      handleEmailBlur,
      handleSubmit,
    },
  };
};
