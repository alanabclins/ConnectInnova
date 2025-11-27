import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom"; // Assumindo react-router-dom
import logoCinnova from "@/assets/logo-nome-cinnova.png";

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  // Se não tiver token na URL, redireciona para login
  useEffect(() => {
    if (!token) {
      navigate("/login");
    }
  }, [token, navigate]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setErrorMessage("As senhas não coincidem.");
      setStatus("error");
      return;
    }

    if (password.length < 6) {
        setErrorMessage("A senha deve ter no mínimo 6 caracteres.");
        setStatus("error");
        return;
    }

    setIsLoading(true);
    setStatus("idle");

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            token: token, 
            new_password: password 
        }),
      });

      if (response.ok) {
        setStatus("success");
        // Opcional: Redirecionar automaticamente após alguns segundos
        setTimeout(() => navigate("/login"), 3000);
      } else {
        const data = await response.json();
        setErrorMessage(data.detail || "Erro ao redefinir senha. O link pode ter expirado.");
        setStatus("error");
      }
    } catch (error) {
      setErrorMessage("Erro de conexão com o servidor.");
      setStatus("error");
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
            <h2 className="text-2xl font-bold text-gray-900">Redefinir Senha</h2>
            <p className="text-gray-500 mt-2">Crie uma senha forte para sua segurança.</p>
          </div>

          {status === "success" ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center animate-in fade-in">
              <div className="text-green-600 text-5xl mb-4">✓</div>
              <h3 className="text-lg font-semibold text-green-800">Senha Alterada!</h3>
              <p className="text-green-700 mt-2">
                Sua senha foi atualizada com sucesso. Você será redirecionado para o login.
              </p>
              <button 
                onClick={() => navigate("/login")}
                className="mt-4 text-sm font-medium text-green-800 underline"
              >
                Ir para Login agora
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4 mt-4">
              {status === "error" && (
                <div className="p-3 bg-red-50 text-red-700 text-sm rounded border border-red-200">
                  {errorMessage}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nova Senha</label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Confirme a Senha</label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 font-medium disabled:opacity-50 transition-all mt-6"
              >
                {isLoading ? "Salvando..." : "Alterar Senha"}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}