import { RegisterForm } from "@/components/register-form";
import logoCinnova from "@/assets/logo-nome-cinnova.png";

export default function RegisterPage() {
  return (
    <div className="grid min-h-screen xl:grid-cols-2">
      {/* Lado Esquerdo - Branding */}
      <div className="relative hidden xl:flex flex-col p-10 mesh-gradient-bg">
        <div className="flex items-center gap-3">
          <img
            src={logoCinnova}
            alt="Logo Connect Innova"
            className="h-12 object-fit"
          />
        </div>
      </div>

      {/* Lado Direito - Conteúdo de Registro */}
      <div className="flex min-h-screen items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md flex flex-col items-center gap-6">
          {/* Logo para mobile */}
          <img
            src={logoCinnova}
            alt="Logo Connect Innova"
            className="h-12 xl:hidden mix-blend-color-dodge"
          />

          {/* Cabeçalho movido para cá */}
          <div className="flex flex-col items-center gap-2 text-center">
            <h1 className="text-3xl font-extrabold text-foreground">
              Crie sua conta
            </h1>
            <p className="text-sm text-muted-foreground max-w-xs">
              Preencha os campos abaixo para iniciar sua jornada conosco.
            </p>
          </div>

          {/* O formulário agora é "puro" */}
          <RegisterForm />

          {/* Rodapé movido para cá */}
          <div className="text-center text-sm">
            Já tem uma conta?{" "}
            <a href="/" className="underline underline-offset-4">
              Faça login
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
