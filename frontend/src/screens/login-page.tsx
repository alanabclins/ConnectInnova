import { LoginForm } from "@/components/login-form";
import logoCinnova from "@/assets/logo-nome-cinnova.png";

export default function LoginPage() {
  return (
    <div className="grid min-h-screen xl:grid-cols-2">
      <div className="relative hidden xl:flex flex-col p-10 mesh-gradient-bg">
        <div className="flex items-center gap-3">
          <img
            src={logoCinnova}
            alt="Logo Connect Innova"
            className="h-12  object-fit"
          />
        </div>
      </div>

      {/* Right side - Login form */}
      <div className="flex min-h-screen items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md flex flex-col items-center gap-6">
          <img
            src={logoCinnova}
            alt="Logo Connect Innova"
            className="h-12 lg:hidden mix-blend-color-dodge"
          />

          <LoginForm />
        </div>
      </div>
    </div>
  );
}
