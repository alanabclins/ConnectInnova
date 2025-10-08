import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { z, ZodError } from "zod";
import { toast } from "sonner";
import authService from "@/services/auth.service";

// Os schemas podem ficar aqui ou em um arquivo separado de validações
const emailSchema = z.string().email("Formato de email inválido");
const registerSchema = z.object({
  fullName: z.string().min(3, "O nome deve ter no mínimo 3 caracteres"),
  email: z.string().email("Email inválido").min(1, "Email é obrigatório"),
  password: z
    .object({
      length: z
        .boolean()
        .refine((val) => val, {
          message: "A senha deve ter no mínimo 8 caracteres",
        }),
      uppercase: z
        .boolean()
        .refine((val) => val, {
          message: "A senha deve conter uma letra maiúscula",
        }),
      lowercase: z
        .boolean()
        .refine((val) => val, {
          message: "A senha deve conter uma letra minúscula",
        }),
      number: z
        .boolean()
        .refine((val) => val, { message: "A senha deve conter um número" }),
      specialChar: z
        .boolean()
        .refine((val) => val, {
          message: "A senha deve conter um caractere especial",
        }),
    })
    .refine((data) => Object.values(data).every((val) => val), {
      message: "Senha inválida",
    }),
});

export const useRegisterForm = () => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [submitErrors, setSubmitErrors] = useState<{
    fullName?: string;
    email?: string;
    password?: string;
  }>({});
  const [inlineEmailError, setInlineEmailError] = useState<string | null>(null);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
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
      emailSchema.parse(email);
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
      registerSchema.parse({ fullName, email, password: passwordChecks });
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
        } = {};
        error.issues.forEach((issue) => {
          const field = issue.path[0];
          if (field === "fullName") fieldErrors.fullName = issue.message;
          if (field === "email") fieldErrors.email = issue.message;
          if (field === "password")
            fieldErrors.password =
              "Por favor, atenda a todos os critérios de senha.";
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
      showPassword,
      isLoading,
      submitErrors,
      inlineEmailError,
      isPasswordFocused,
      passwordChecks,
    },
    handlers: {
      setFullName,
      setEmail,
      setPassword,
      setShowPassword,
      setIsPasswordFocused,
      handleEmailBlur,
      handleSubmit,
    },
  };
};
