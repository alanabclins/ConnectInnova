import axios from "axios";
import { type User } from "../models/user";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

class AuthService {
  async register(user: User): Promise<any> {
    const response = await axios.post(`${API_URL}/users`, user);
    return response.data;
  }

  async login(data: FormData): Promise<any> {
    const response = await axios.post(`${API_URL}/login/access-token`, data);

    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
    }

    return response.data;
  }

  async refreshToken(): Promise<any> {
    const response = await axios.get(`${API_URL}/login/refresh-token`, {
      withCredentials: true,
    });

    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
    }

    return response.data;
  }

  logout(): void {
    localStorage.removeItem("token");
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem("token");
  }
}

export default new AuthService();
