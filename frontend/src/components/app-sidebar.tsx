"use client";

import * as React from "react";
import {
  IconHome,
  IconBook,
  IconCompass,
  IconTarget,
  IconFileText,
  IconChevronLeft,
} from "@tabler/icons-react";
import { cn } from "@/lib/utils";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";

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
  return (
    <Sidebar collapsible="icon" {...props}>
      {/* Cabeçalho com brand */}
      <SidebarHeader>
        <div className="flex items-center gap-3 p-4">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <div className="w-4 h-4 bg-primary-foreground rounded-sm"></div>
          </div>
          <div>
            <h1 className="text-lg font-semibold text-foreground">Connect</h1>
            <p className="text-sm text-muted-foreground">Innova</p>
          </div>
        </div>
      </SidebarHeader>

      {/* Navegação principal */}
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

      {/* Rodapé com usuário */}
      <SidebarFooter>
        <div className="flex items-center justify-between bg-sidebar-item rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-muted rounded-lg flex items-center justify-center">
              <span className="text-sm font-medium text-foreground">L</span>
            </div>
            <div>
              <p className="font-medium text-foreground">Lucas</p>
              <p className="text-xs text-muted-foreground">AgroPlus</p>
            </div>
          </div>
          <IconChevronLeft
            size={16}
            stroke={1.5}
            className="text-muted-foreground"
          />
        </div>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
