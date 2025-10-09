import {
  createContext,
  type FC,
  useState,
  type ReactNode,
  useContext,
  useEffect,
} from "react";
import userService from "../services/user.service";
import authService from "../services/auth.service";
import { type User } from "../models/user";

interface AuthContextType {
  user: User | undefined;
  setUser: (user: User | undefined) => void;
  login: (data: FormData) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

interface AuthContextProviderProps {
  children: ReactNode;
}

const fakeUser: User = {
  uuid: "1",
  first_name: "Usuário",
  last_name: "Fake",
  is_active: true,
  password: "abc123",
  email: "fakeuser@example.com",
};

const AuthProvider: FC<AuthContextProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User>();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkUserAuthentication();
  }, []);

  const checkUserAuthentication = async (): Promise<void> => {
    try {
      const userProfile = await userService.getProfile();
      setUser(userProfile);
    } catch {
      // setUser(fakeUser);
      setUser(undefined);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (data: FormData): Promise<void> => {
    await authService.login(data);
    const userProfile = await userService.getProfile();
    setUser(userProfile);
  };

  const logout = (): void => {
    authService.logout();
    setUser(undefined);
  };

  const contextValue: AuthContextType = {
    user,
    setUser,
    login,
    logout,
    isLoading,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export { AuthProvider, useAuth };
