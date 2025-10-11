import { cn } from "@/lib/utils";
import { CheckCircle2, XCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

type PasswordChecks = {
  length: boolean;
  uppercase: boolean;
  lowercase: boolean;
  number: boolean;
  specialChar: boolean;
};

interface PasswordStrengthProps {
  passwordChecks: PasswordChecks;
}

const PasswordRequirement = ({
  isValid,
  label,
}: {
  isValid: boolean;
  label: string;
}) => (
  <li
    className={cn(
      "flex items-center text-sm",
      isValid ? "text-green-600" : "text-muted-foreground"
    )}
  >
    {isValid ? (
      <CheckCircle2 className="mr-2 h-4 w-4" />
    ) : (
      <XCircle className="mr-2 h-4 w-4" />
    )}
    {label}
  </li>
);

export const PasswordStrength = ({ passwordChecks }: PasswordStrengthProps) => (
  <Alert>
    <AlertTitle>Requisitos da Senha</AlertTitle>
    <AlertDescription>
      <ul className="mt-2 space-y-1">
        <PasswordRequirement
          label="Pelo menos 8 caracteres"
          isValid={passwordChecks.length}
        />
        <PasswordRequirement
          label="Uma letra maiúscula (A-Z)"
          isValid={passwordChecks.uppercase}
        />
        <PasswordRequirement
          label="Uma letra minúscula (a-z)"
          isValid={passwordChecks.lowercase}
        />
        <PasswordRequirement
          label="Um número (0-9)"
          isValid={passwordChecks.number}
        />
        <PasswordRequirement
          label="Um caractere especial (!@#$...)"
          isValid={passwordChecks.specialChar}
        />
      </ul>
    </AlertDescription>
  </Alert>
);
