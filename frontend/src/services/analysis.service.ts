import axios from "axios";

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
        customPrompt ? customPrompt : "",
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
        "Erro ao chamar o endpoint de análise:",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao realizar análise do projeto. Verifique o servidor ou o ID informado."
      );
    }
  }

  async feedbackAnalysis(feedback_uuid: string) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.get(
        `${API_URL}/feedback/${feedback_uuid}`,
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
        "Erro ao chamar o endpoint de análise:",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao realizar análise do projeto. Verifique o servidor ou o ID informado."
      );
    }
  }

 async resumAnalysis(resum_uuid: string) {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("No authentication token found");
    }

    try {
      const response = await axios.get(
      `${API_URL}/resum/${resum_uuid}`,
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
        "Erro ao chamar o endpoint de análise:",
        error.response?.data || error.message
      );
      throw new Error(
        error.response?.data?.detail ||
          "Erro ao realizar análise do projeto. Verifique o servidor ou o ID informado."
      );
    }
  }

}

export default new AnalysisService();
