import axios from "axios";
import { type User } from "../models/user";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

class UserService {
  async getProfile(): Promise<User> {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    const response = await axios.get(`${API_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.data;
  }
}

export default new UserService();
