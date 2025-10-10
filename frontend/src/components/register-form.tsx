import { Eye, EyeOff } from "lucide-react";
import { cn } from "@/lib/utils";
import { useRegisterForm } from "@/hooks/useRegisterForm";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "./ui/shadcn-io/spinner";
import { PasswordStrength } from "@/components/ui/passwordStrength";

export function RegisterForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const { models, handlers } = useRegisterForm();
  const {
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
  } = models;
  const {
    setFullName,
    setEmail,
    setPassword,
    setConfirmPassword,
    setShowPassword,
    setShowPasswordRequirements,
    handleEmailBlur,
    handleSubmit,
  } = handlers;

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("w-full", className)}
      {...props}
    >
      <div className="grid gap-6">
        {/* Campo Nome Completo */}
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

        {/* Campo Email */}
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

        {/* Agrupamento dos campos de senha para controlar o foco */}
        <div
          className="grid gap-6" // Aumentado o gap interno para manter a consistência visual
          onFocus={() => setShowPasswordRequirements(true)}
          onBlur={() => setShowPasswordRequirements(false)}
        >
          {/* Campo Senha */}
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

          {/* Campo Confirmar Senha */}
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

        {/* Requisitos da senha */}
        {(showPasswordRequirements || submitErrors.password) && (
          <PasswordStrength passwordChecks={passwordChecks} />
        )}

        {/* Botão de Cadastro */}
        <Button
          type="submit"
          className="w-full"
          disabled={isLoading}
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
