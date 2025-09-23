import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background text-foreground px-4">
      <h1 className="text-6xl font-extrabold mb-4 animate-pulse text-primary">
        404
      </h1>
      <p className="text-xl mb-8 text-center animate-fade-in">
        Ops! A página que você está procurando não existe.
      </p>
      <div className="flex gap-4">
        <Button variant="default" onClick={() => navigate("/")}>
          Voltar para Home
        </Button>
        <Button variant="secondary" onClick={() => navigate(-1)}>
          Voltar
        </Button>
      </div>
    </div>
  );
}
