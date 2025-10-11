"use client";

import {
  IconHome,
  IconBook,
  IconCompass,
  IconTarget,
  IconFileText,
  IconChevronLeft,
  IconLogout,
} from "@tabler/icons-react";
import { cn } from "@/lib/utils";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
import { useAuth } from "@/auth/authContext";
import { ConfirmationDialog } from "@/components/ui/confirmationDialog";
import * as React from "react";

// 1. A importação do 'next/image' foi REMOVIDA

// Import da sua logo (isso continua igual e correto)
import logoCinnova from "@/assets/logo-nome-cinnova.png";

interface NavItem {
  icon: React.ElementType;
  label: string;
  active?: boolean;
}

const navItems: NavItem[] = [
  { icon: IconHome, label: "Início", active: true },
  { icon: IconBook, label: "Minha trilha" },
  { icon: IconCompass, label: "Explorar projetos" },
  { icon: IconTarget, label: "Desafios" },
  { icon: IconFileText, label: "Editais" },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { user, logout } = useAuth();
  const [isLogoutDialogOpen, setLogoutDialogOpen] = React.useState(false);

  return (
    <>
      <Sidebar collapsible="icon" {...props}>
        {/* Cabeçalho com brand */}
        <SidebarHeader>
          <div className="p-4">
            {/* 2. O componente <Image> foi substituído pela tag <img> */}
            <img
              src={logoCinnova}
              alt="Logotipo da C-Innova"
              className="h-8 w-auto" // As mesmas classes de estilo funcionam
            />
          </div>
        </SidebarHeader>

        {/* O resto do componente continua igual... */}
        <SidebarContent>
          <nav className="flex-1 px-2">
            <ul className="space-y-2">
              {navItems.map((item, index) => {
                const Icon = item.icon;
                return (
                  <li key={index}>
                    <button
                      className={cn(
                        "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200",
                        item.active
                          ? "bg-primary text-primary-foreground shadow-lg"
                          : "text-muted-foreground hover:bg-sidebar-item-hover hover:text-foreground"
                      )}
                    >
                      <Icon size={20} stroke={1.5} />
                      <span className="font-medium">{item.label}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </nav>
        </SidebarContent>

        <SidebarFooter>
          <div className="flex items-center justify-between bg-sidebar-item rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-muted rounded-lg flex items-center justify-center">
                <span className="text-sm font-medium text-foreground">
                  {user?.first_name?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="max-w-[130px]">
                <p className="font-medium text-foreground truncate">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  AgroPlus
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <IconChevronLeft
                size={16}
                stroke={1.5}
                className="text-muted-foreground"
              />
              <button
                onClick={() => setLogoutDialogOpen(true)}
                className="text-muted-foreground hover:text-red-500 transition-colors"
                aria-label="Sair"
              >
                <IconLogout size={16} stroke={1.5} />
              </button>
            </div>
          </div>
        </SidebarFooter>

        <SidebarRail />
      </Sidebar>

      <ConfirmationDialog
        isOpen={isLogoutDialogOpen}
        onOpenChange={setLogoutDialogOpen}
        title="Confirmar Saída"
        description="Você tem certeza que deseja encerrar a sessão?"
        onConfirm={logout}
        confirmText="Sim, Sair"
        variant="destructive"
      />
    </>
  );
}
