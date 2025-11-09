import { useState, useMemo } from "react";
import { toast } from "sonner";
import { Eye, EyeOff } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "./ui/shadcn-io/spinner";
import { PasswordStrength } from "@/components/ui/passwordStrength";
import authService from "@/services/auth.service";
import axios from "axios";

interface FormErrors {
  [key: string]: string;
}

export function RegisterForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [submitErrors, setSubmitErrors] = useState<FormErrors>({});
  const [inlineEmailError, setInlineEmailError] = useState("");
  const [showPasswordRequirements, setShowPasswordRequirements] =
    useState(false);

  const passwordChecks = useMemo(() => {
    return {
      length: password.length >= 8 && password.length <= 14,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      specialChar: /[^A-Za-z0-9]/.test(password),
    };
  }, [password]);

  const isFormValid = useMemo(() => {
    const allReqsMet = Object.values(passwordChecks).every(Boolean);
    return allReqsMet && password === confirmPassword && password !== "";
  }, [password, confirmPassword, passwordChecks]);

  const handleEmailBlur = () => {
    const emailRegex =
      /^[^\s\[\]\(\)\{\}<>]+@[^\s\[\]\(\)\{\}<>]+\.[^\s\[\]\(\)\{\}<>]+$/;
    if (email && !/^\S+@\S+\.\S+$/.test(email)) {
      setInlineEmailError("Por favor, insira um email válido.");
    } else if (email && !emailRegex.test(email)) {
      setInlineEmailError(
        "Por favor, insira um email válido e sem caracteres especiais como (), {}, [], <>."
      );
    } else {
      setInlineEmailError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitErrors({});
    setInlineEmailError("");

    if (!isFormValid) {
      toast.error("Formulário inválido", {
        description: "Por favor, verifique os requisitos da senha.",
      });
      return;
    }

    setIsLoading(true);

    const names = fullName.trim().split(" ");
    const firstName = names[0];
    const lastName = names.length > 1 ? names.slice(1).join(" ") : "";

    const user = {
      name: fullName,
      first_name: firstName,
      last_name: lastName,
      email,
      password,
    };

    try {
      await authService.register(user);
      toast.success("Conta criada com sucesso!", {
        description: "Você será redirecionado para a tela de login.",
      });
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        const newErrors: FormErrors = {};
        let toastDescription = "Por favor, corrija os erros indicados.";

        if (typeof error.response.data.detail === "string") {
          toastDescription = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          error.response.data.detail.forEach((err: any) => {
            if (err.loc && err.loc.length > 1) {
              const field = err.loc[1];
              newErrors[field] = err.msg;
            }
          });
          setSubmitErrors(newErrors);
        }

        toast.error("Falha no cadastro", {
          description: toastDescription,
        });
      } else {
        toast.error("Erro ao criar a conta", {
          description:
            "Ocorreu um erro inesperado. Tente novamente mais tarde.",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("w-full", className)}
      {...props}
    >
      <div className="grid gap-6">
        <div className="grid gap-3">
          <Label htmlFor="fullName">Nome completo</Label>
          <Input
            id="fullName"
            type="text"
            placeholder="Seu nome completo"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            disabled={isLoading}
            required
            className={cn(
              submitErrors.fullName &&
                "border-destructive focus-visible:ring-destructive"
            )}
          />
          {submitErrors.fullName && (
            <p className="text-sm text-destructive">{submitErrors.fullName}</p>
          )}
        </div>

        <div className="grid gap-3">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="m@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onBlur={handleEmailBlur}
            disabled={isLoading}
            required
            className={cn(
              (submitErrors.email || inlineEmailError) &&
                "border-destructive focus-visible:ring-destructive"
            )}
          />
          {submitErrors.email ? (
            <p className="text-sm text-destructive">{submitErrors.email}</p>
          ) : inlineEmailError ? (
            <p className="text-sm text-destructive">{inlineEmailError}</p>
          ) : null}
        </div>

        <div
          className="grid gap-6"
          onFocus={() => setShowPasswordRequirements(true)}
          onBlur={() => setShowPasswordRequirements(false)}
        >
          <div className="grid gap-3">
            <Label htmlFor="password">Senha</Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Crie uma senha forte"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
                required
                className={cn(
                  "pr-10",
                  submitErrors.password &&
                    "border-destructive focus-visible:ring-destructive"
                )}
              />
              <button
                type="button"
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                aria-label={showPassword ? "Esconder senha" : "Mostrar senha"}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>
            {submitErrors.password && (
              <p className="text-sm text-destructive">
                {submitErrors.password}
              </p>
            )}
          </div>

          <div className="grid gap-3">
            <Label htmlFor="confirmPassword">Confirmar senha</Label>
            <div className="relative">
              <Input
                id="confirmPassword"
                type={showPassword ? "text" : "password"}
                placeholder="Repita sua senha"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={isLoading}
                required
                className={cn(
                  "pr-10",
                  submitErrors.confirmPassword &&
                    "border-destructive focus-visible:ring-destructive"
                )}
              />
              <button
                type="button"
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                aria-label={showPassword ? "Esconder senha" : "Mostrar senha"}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>
            {submitErrors.confirmPassword && (
              <p className="text-sm text-destructive">
                {submitErrors.confirmPassword}
              </p>
            )}
          </div>
        </div>

        {(showPasswordRequirements || submitErrors.password) && (
          <PasswordStrength passwordChecks={passwordChecks} />
        )}

        <Button
          type="submit"
          className="w-full"
          disabled={isLoading || !isFormValid}
          onMouseDown={(e) => e.preventDefault()}
        >
          {isLoading ? (
            <>
              <Spinner variant={"circle"} /> Cadastrando...
            </>
          ) : (
            "Criar conta"
          )}
        </Button>
      </div>
    </form>
  );
}
