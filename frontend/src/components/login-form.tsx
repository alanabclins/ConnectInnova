import { useState } from "react";
import { replace, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import authService from "@/services/auth.service";
import { z, ZodError } from "zod";
import { cn } from "@/lib/utils";
import { Spinner } from "./ui/shadcn-io/spinner";

const loginSchema = z.object({
  email: z.string().email("Email inválido").min(1, "Email é obrigatório"),
  password: z.string().min(6, "A senha deve ter no mínimo 6 caracteres"),
});

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>(
    {}
  );
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setIsLoading(true);

    try {
      const validatedData = loginSchema.parse({ email, password });

      // Cria FormData para enviar ao backend
      const formData = new FormData();
      formData.append("username", validatedData.email);
      formData.append("password", validatedData.password);

      // Chama o login do contexto, que atualiza o user
      await authService.login(formData);

      toast.success("Login realizado com sucesso!", {
        description: "Redirecionando...",
      });

      setTimeout(() => {
        window.location.href = "/home";
      }, 1000);
    } catch (error) {
      if (error instanceof ZodError) {
        const fieldErrors: { email?: string; password?: string } = {};
        error.issues.forEach((issue) => {
          const field = issue.path[0];
          if (field === "email") fieldErrors.email = issue.message;
          if (field === "password") fieldErrors.password = issue.message;
        });
        setErrors(fieldErrors);

        toast.error("Erro de validação", {
          description: error.issues[0]?.message,
        });
      } else if ((error as any)?.response?.status === 401) {
        toast.error("Email ou senha incorretos");
      } else {
        toast.error("Erro ao fazer login", {
          description:
            (error as any)?.response?.data?.detail ||
            "Tente novamente mais tarde",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("flex flex-col gap-6", className)}
      {...props}
    >
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-3xl font-extrabold text-foreground">Bem-vindo!</h1>
        <p className="text-sm text-muted-foreground max-w-xs">
          Seu projeto está prestes a se tornar algo incrível.
        </p>
      </div>

      <div className="grid gap-6">
        <div className="grid gap-3">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="m@example.com"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setErrors((prev) => ({ ...prev, email: undefined }));
            }}
            disabled={isLoading}
            required
            className={cn(
              errors.email &&
                "border-destructive focus-visible:ring-destructive"
            )}
          />
          {errors.email && (
            <p className="text-sm text-destructive">{errors.email}</p>
          )}
        </div>

        <div className="grid gap-3">
          <div className="flex items-center">
            <Label htmlFor="password">Password</Label>
            <a
              href="/forgot-password"
              className="ml-auto text-sm underline-offset-4 hover:underline"
            >
              Forgot your password?
            </a>
          </div>
          <Input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setErrors((prev) => ({ ...prev, password: undefined }));
            }}
            disabled={isLoading}
            required
            className={cn(
              errors.password &&
                "border-destructive focus-visible:ring-destructive"
            )}
          />
          {errors.password && (
            <p className="text-sm text-destructive">{errors.password}</p>
          )}
        </div>

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? (
            <>
              {/* <Loader2 className="mr-2 h-4 w-4 animate-spin" /> */}
              <Spinner variant={"circle"} />
              Loading...
            </>
          ) : (
            "Login"
          )}
        </Button>

        <div className="text-center text-sm">
          Don&apos;t have an account?{" "}
          <a href="/register" className="underline underline-offset-4">
            Sign up
          </a>
        </div>
      </div>
    </form>
  );
}
