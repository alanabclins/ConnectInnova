import type { ProjectFormData } from "@/hooks/useProjectForm";
import axios from "axios";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

class ProjectService {
  async createProject(projectData: any): Promise<any> {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.post(`${API_URL}/projects`, projectData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data; // A ideia é o uuid vir por aqui
    } catch (error: any) {
      console.error("Erro ao criar projeto:", error);
      throw error;
    }
  }

  async getProjectDetails(projectUuid: string): Promise<any> {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(
        `${API_URL}/projects/${projectUuid}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (error: any) {
      console.error("Erro ao buscar detalhes do projeto:", error);
      throw error;
    }
  }

  async updateProject(
    projectUuid: string,
    projectData: ProjectFormData
  ): Promise<any> {
    try {
      const token = localStorage.getItem("token");
      
      const response = await axios.patch(
        `${API_URL}/projects/${projectUuid}`,
        projectData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      return response.data;
    } catch (error: any) {
      console.error("Erro ao atualizar projeto:", error);
      throw error;
    }
  }

  async getProjects(): Promise<any[]> {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(`${API_URL}/projects`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      console.error("Erro ao buscar projetos:", error);
      throw error;
    }
  }

  async deleteProject(projectId: string): Promise<any> {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.delete(`${API_URL}/projects/${projectId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      console.error("Erro ao deletar projeto:", error);
      throw error;
    }
  }
}

export default new ProjectService();
