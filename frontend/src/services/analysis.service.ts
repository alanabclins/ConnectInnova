import axios from "axios";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

class AnalysisService {
  // Chamada POST para INICIAR a análise completa (15 critérios)
  async generateFullAnalysis(project_uuid: string) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.post(
        `${API_URL}/feedback/${project_uuid}`,
        null, // Corpo da requisição vazio, conforme seu exemplo cURL: -d ''
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );

      return response.data;
    } catch (error: any) {
      console.error(
        "Erro ao gerar análise completa (POST):",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao gerar análise completa. Verifique o servidor."
      );
    }
  }

  async getFeedback(project_uuid: string, regenerate: boolean = false) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.get(
      `${API_URL}/feedback/${project_uuid}?regenerate=${regenerate}`,
      {
        headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json",
        },
      }
      );

      return response.data;
    } catch (error: any) {
      console.error(
        "Erro ao buscar análise (GET):",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao buscar análise. O documento de Feedback/Análise pode não ter sido criado."
      );
    }
  }

 async resumAnalysis(project_uuid: string) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.get(
      `${API_URL}/resum/${project_uuid}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        },
      }
    );

      return response.data;
    } catch (error: any) {
      console.error(
        "Erro ao chamar o endpoint de resumo:",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao realizar resumo do projeto. Verifique o servidor."
      );
    }
  }

}

export default new AnalysisService();