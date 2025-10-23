import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  IconHome,
  IconBook,
  IconCompass,
  IconTarget,
  IconFileText,
  IconChevronLeft,
  IconLogout,
} from "@tabler/icons-react";
import { LogOut, ChevronsUpDown, BadgeCheck, Bell } from "lucide-react";

import { cn } from "@/lib/utils";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  useSidebar,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useAuth } from "@/auth/authContext";
import { ConfirmationDialog } from "@/components/ui/confirmationDialog";
import logoCinnova from "@/assets/logo-nome-cinnova.png";
import logo from "@/assets/logo-cinnova.png";

interface NavItem {
  icon: React.ElementType;
  label: string;
  clickLink?: string;
}

const navItems: NavItem[] = [
  { icon: IconHome, label: "Início", clickLink: "/home" },
  { icon: IconBook, label: "Minha trilha", clickLink: "/minha-trilha" },
  { icon: IconCompass, label: "Explorar projetos", clickLink: "/explorar" },
  { icon: IconTarget, label: "Desafios", clickLink: "/desafios" },
  { icon: IconFileText, label: "Editais", clickLink: "/editais" },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { user, logout } = useAuth();
  const [isLogoutDialogOpen, setLogoutDialogOpen] = React.useState(false);

  const { state, toggleSidebar, isMobile } = useSidebar();
  const isCollapsed = state === "collapsed";

  const navigate = useNavigate();
  const location = useLocation();
  const pathname = location.pathname;

  const handleTabClick = (href: string) => {
    navigate(href);
  };

  const userFullname = [user?.first_name, user?.last_name]
    .filter(Boolean)
    .join(" ");
  const userFallback =
    (user?.first_name?.charAt(0) || "") + (user?.last_name?.charAt(0) || "");

  return (
    <>
      <Sidebar collapsible="icon" {...props}>
        <SidebarHeader>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                size="lg"
                className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                tooltip="Connect Innova"
              >
                <div className="text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <img src={logo} alt="C-Innova" className="size-8" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">Connect</span>
                  <span className="truncate font-medium">Innova</span>
                </div>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarHeader>

        <SidebarContent>
          <SidebarMenu className="flex-1">
            {navItems.map((item, index) => {
              const Icon = item.icon;
              const isActive = !!item.clickLink && pathname === item.clickLink;

              return (
                <SidebarMenuItem key={index} className="px-2 mb-2">
                  <SidebarMenuButton
                    onClick={() => handleTabClick(item.clickLink!)}
                    disabled={!item.clickLink}
                    isActive={isActive}
                    tooltip={item.label}
                    className={cn(
                        "w-full flex items-center gap-3 px-4 py-3 rounded-md transition-all duration-200",
                        isActive
                          ? "bg-primary text-primary-foreground shadow-lg !bg-primary"
                          : "text-muted-foreground hover:bg-sidebar-item-hover hover:text-foreground"
                      )}
                  >
                    <Icon size={20} stroke={1.5} />
                    <span className="font-medium">{item.label}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              );
            })}
          </SidebarMenu>
        </SidebarContent>

        <SidebarFooter>
          <SidebarMenu>
            <SidebarMenuItem>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <SidebarMenuButton
                    size="lg"
                    className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                    tooltip={userFullname || "Menu do Usuário"}
                  >
                    <Avatar className="h-8 w-8 rounded-lg">
                      <AvatarImage src={user?.picture} alt={userFullname} />
                      <AvatarFallback className="rounded-lg">
                        {userFallback.toUpperCase() || "U"}
                      </AvatarFallback>
                    </Avatar>
                    <div className="grid flex-1 text-left text-sm leading-tight">
                      <span className="truncate font-medium">
                        {userFullname}
                      </span>
                      <span className="truncate text-xs">{user?.email}</span>
                    </div>
                    <ChevronsUpDown className="ml-auto size-4" />
                  </SidebarMenuButton>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  className="w-[var(--radix-dropdown-menu-trigger-width)] min-w-56 rounded-lg"
                  side={isMobile ? "bottom" : "right"}
                  align="end"
                  sideOffset={4}
                >
                  <DropdownMenuLabel className="p-0 font-normal">
                    <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                      <Avatar className="h-8 w-8 rounded-lg">
                        <AvatarImage src={user?.picture} alt={userFullname} />
                        <AvatarFallback className="rounded-lg">
                          {userFallback.toUpperCase() || "U"}
                        </AvatarFallback>
                      </Avatar>
                      <div className="grid flex-1 text-left text-sm leading-tight">
                        <span className="truncate font-medium">
                          {userFullname}
                        </span>
                        <span className="truncate text-xs">{user?.email}</span>
                      </div>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuGroup>
                    <DropdownMenuItem>
                      <BadgeCheck className="mr-2 size-4" />
                      Account
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Bell className="mr-2 size-4" />
                      Notifications
                    </DropdownMenuItem>
                  </DropdownMenuGroup>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => setLogoutDialogOpen(true)}>
                    <LogOut className="mr-2 size-4" />
                    Log out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                onClick={toggleSidebar}
                tooltip={isCollapsed ? "Expandir" : "Recolher"}
              >
                <IconChevronLeft
                  size={16}
                  stroke={1.5}
                  className={cn(
                    "transition-transform duration-300",
                    isCollapsed && "rotate-180"
                  )}
                />
                <span>{isCollapsed ? "Expandir" : "Recolher"}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
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
