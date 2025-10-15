import axios from "axios";

// Assuma que esta variável de ambiente está configurada (ex: VITE_BACKEND_API_URL=http://127.0.0.1:8000/api/v1)
const API_URL = import.meta.env.VITE_BACKEND_API_URL;

class AnalysisService {
  async analyzeProject(projectId: string, customPrompt?: string) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.post(
        `${API_URL}/analysis/${projectId}`,
        customPrompt ? { custom_prompt: customPrompt } : {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      return response.data;
    } catch (error: any) {
      console.error("Erro ao chamar o endpoint de análise:", error.response?.data || error.message);
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao realizar análise do projeto. Verifique o servidor ou o ID informado."
      );
    }
  }
}

export default new AnalysisService();