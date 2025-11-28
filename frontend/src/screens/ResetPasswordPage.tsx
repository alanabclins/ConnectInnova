import { useState, useEffect, useMemo } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { toast } from "sonner"; // Assumindo que você usa sonner como no registro
import { Eye, EyeOff } from "lucide-react";

// Componentes UI e Utils
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/ui/shadcn-io/spinner"; // Ajuste o caminho se necessário
import { PasswordStrength } from "@/components/ui/passwordStrength";

// Assets
import logoCinnova from "@/assets/logo-nome-cinnova.png";

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  // Estados do Formulário
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success">("idle");
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);

  // Se não tiver token na URL, redireciona para login
  useEffect(() => {
    if (!token) {
      toast.error("Token inválido ou ausente.");
      navigate("/login");
    }
  }, [token, navigate]);

  // Lógica de Validação (Copiada do RegisterForm)
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

  // Handler de Envio
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!isFormValid) {
      toast.error("Formulário inválido", {
        description: "Verifique os requisitos da senha e se elas coincidem.",
      });
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/login/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: token,
          new_password: password,
        }),
      });

      if (response.ok) {
        setStatus("success");
        toast.success("Senha alterada com sucesso!");
        // Redireciona após 3 segundos
        setTimeout(() => navigate("/login"), 3000);
      } else {
        const data = await response.json();
        toast.error("Erro ao redefinir senha", {
            description: data.detail || "O link pode ter expirado.",
        });
      }
    } catch (error) {
      toast.error("Erro de conexão", {
        description: "Não foi possível conectar ao servidor.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen xl:grid-cols-2">
      {/* Lado Esquerdo (Igual ao Login) */}
      <div className="relative hidden xl:flex flex-col p-10 mesh-gradient-bg">
        <div className="flex items-center gap-3">
          <img src={logoCinnova} alt="Logo" className="h-12 object-fit" />
        </div>
        <div className="flex-1 flex items-center justify-center text-white p-10">
          <h1 className="text-4xl font-bold">Defina sua nova senha</h1>
        </div>
      </div>

      {/* Lado Direito - Formulário */}
      <div className="flex min-h-screen items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md flex flex-col gap-6">
          
          {/* Logo Mobile */}
          <div className="xl:hidden flex justify-center mb-4">
            <img src={logoCinnova} alt="Logo" className="h-10" />
          </div>

          <div className="text-center">
            <h2 className="text-2xl font-bold text-900">Redefinir Senha</h2>
            <p className="text-500 mt-2">Crie uma senha forte para sua segurança.</p>
          </div>

          {status === "success" ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center animate-in fade-in zoom-in duration-300">
              <div className="text-green-600 text-5xl mb-4">✓</div>
              <h3 className="text-lg font-semibold text-green-800">Tudo pronto!</h3>
              <p className="text-green-700 mt-2">
                Sua senha foi atualizada. Você será redirecionado para o login.
              </p>
              <Button
                variant="link"
                onClick={() => navigate("/login")}
                className="mt-4 text-green-800"
              >
                Ir para Login agora
              </Button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6 mt-4">
              
              {/* Campo: Nova Senha */}
              <div 
                className="grid gap-3"
                onFocus={() => setShowPasswordRequirements(true)}
                onBlur={() => setShowPasswordRequirements(false)}
              >
                <Label htmlFor="password">Nova Senha</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Crie uma senha forte"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading}
                    required
                    className="pr-10"
                  />
                  <button
                    type="button"
                    onMouseDown={(e) => e.preventDefault()} // Evita perder o foco do input
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
              </div>

              {/* Campo: Confirmar Senha */}
              <div className="grid gap-3"
                    onFocus={() => setShowPasswordRequirements(true)}
                    onBlur={() => setShowPasswordRequirements(false)}
                    >
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
                        confirmPassword && password !== confirmPassword && "border-destructive focus-visible:ring-destructive"
                    )}
                  />
                  <button
                    type="button"
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
                {confirmPassword && password !== confirmPassword && (
                    <p className="text-sm text-destructive">As senhas não coincidem.</p>
                )}
              </div>

              {/* Força da Senha (Condicional) */}
              {(showPasswordRequirements || password) && (
                 <PasswordStrength passwordChecks={passwordChecks} />
              )}

              {/* Botão de Envio */}
              <Button
                type="submit"
                className="w-full"
                disabled={isLoading || !isFormValid}
              >
                {isLoading ? (
                  <>
                    <Spinner className="mr-2" /> Salvando...
                  </>
                ) : (
                  "Alterar Senha"
                )}
              </Button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}