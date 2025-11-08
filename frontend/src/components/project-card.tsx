import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button"; // 1. Import do Botão
import {
  IconCalendar,
  IconFileText,
  IconTrash, // 1. Import do Ícone de Lixeira
} from "@tabler/icons-react";
import React from "react"; // Import do React para o MouseEvent

interface ProjectCardProps {
  id: string;
  name: string;
  description?: string;
  createdAt?: string;
  onClick?: () => void;
  onDelete: () => void; // 2. Adição da prop onDelete
}

export const ProjectCard = ({
  name,
  description,
  createdAt,
  onClick,
  onDelete, // 2. Recebendo a prop
}: ProjectCardProps) => {
  /**
   * 3. Handler para o clique no botão de deletar.
   * Impede que o evento de clique "vaze" para o Card principal (o que
   * acionaria a navegação para o dashboard).
   */
  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete();
  };

  return (
    <Card
      onClick={onClick}
      className="w-full h-full max-h-48 cursor-pointer bg-card hover:bg-card/90 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg overflow-hidden group flex flex-col"
    >
      {/* 4. Mudei de px-6 para p-6 para dar padding vertical também */}
      <div className="flex flex-col justify-between flex-1 p-6">
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <IconFileText className="w-5 h-5 text-primary mt-1 flex-shrink-0" />
            <h3 className="text-lg font-semibold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
              {name}
            </h3>
          </div>
          {description && (
            <p className="text-sm text-muted-foreground line-clamp-3 leading-relaxed">
              {description}
            </p>
          )}
        </div>

        {/* 4. Modificação do rodapé */}
        <div className="flex items-center justify-between mt-4">
          {/* Lado Esquerdo: Data (condicional) */}
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            {createdAt && (
              <>
                <IconCalendar className="w-4 h-4" />
                <span>{new Date(createdAt).toLocaleDateString("pt-BR")}</span>
              </>
            )}
          </div>

          {/* Lado Direito: Botão Deletar (sempre visível) */}
          <Button
            variant="ghost"
            size="icon"
            className="text-destructive hover:bg-destructive/10 h-8 w-8" // Tamanho menor
            onClick={handleDeleteClick}
            aria-label="Deletar projeto"
          >
            <IconTrash className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
};
