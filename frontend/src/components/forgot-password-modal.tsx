import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { z, ZodError } from "zod";
import { Spinner } from "@/components/ui/shadcn-io/spinner"; // Ajuste o caminho se necessário
import { X } from "lucide-react"; // Ícone de fechar (instale lucide-react se não tiver)

const resetSchema = z.object({
  email: z.string().email("Email inválido").min(1, "Email é obrigatório"),
});

interface ForgotPasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ForgotPasswordModal({ isOpen, onClose }: ForgotPasswordModalProps) {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // 1. Validação local
      resetSchema.parse({ email });

      // 2. Chamada à API
      // OBS: Certifique-se que VITE_API_URL está no seu .env
      const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/request-password-reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) throw new Error("Erro ao conectar com servidor");

      // 3. Sucesso
      toast.success("Link enviado!", {
        description: "Se o email existir, você receberá instruções em breve.",
      });
      
      setEmail(""); // Limpa o campo
      onClose(); // Fecha o modal

    } catch (err) {
      if (err instanceof ZodError) {
        setError(err.issues[0].message);
      } else {
        setError("Não foi possível enviar a solicitação. Tente novamente.");
        toast.error("Erro no envio");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-md rounded-lg border bg-background p-6 shadow-lg animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Botão Fechar */}
        <button 
          onClick={onClose}
          className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        >
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </button>

        <div className="flex flex-col space-y-1.5 text-center sm:text-left mb-4">
          <h2 className="text-lg font-semibold leading-none tracking-tight">Recuperar Senha</h2>
          <p className="text-sm text-muted-foreground">
            Digite seu email para receber o link de redefinição.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="reset-email">Email</Label>
            <Input
              id="reset-email"
              type="email"
              placeholder="m@example.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setError(null);
              }}
              disabled={isLoading}
              className={error ? "border-destructive focus-visible:ring-destructive" : ""}
            />
            {error && <p className="text-sm text-destructive font-medium">{error}</p>}
          </div>

          <div className="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 gap-2">
            <Button variant="outline" type="button" onClick={onClose} disabled={isLoading}>
              Cancelar
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Spinner variant="circle" className="mr-2 h-4 w-4" />
                  Enviando...
                </>
              ) : (
                "Enviar Link"
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}