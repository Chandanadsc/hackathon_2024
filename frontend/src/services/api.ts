import axios from "axios";
import { Document, AuthResponse, User } from "../types";

// Get API URL from environment variables with fallback
const API_URL = process.env.REACT_APP_API_URL;
if (!API_URL) {
  console.warn(
    "REACT_APP_API_URL not set, using default: http://localhost:5000"
  );
}

const api = axios.create({
  baseURL: API_URL || "http://localhost:5000",
});

// Add request interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signin: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post("/api/auth/signin", { email, password });
    return response.data;
  },

  signup: async (
    name: string,
    email: string,
    password: string
  ): Promise<AuthResponse> => {
    const response = await api.post("/api/auth/signup", {
      name,
      email,
      password,
    });
    return response.data;
  },

  updateProfile: async (updateData: {
    name?: string;
    currentPassword?: string;
    newPassword?: string;
  }): Promise<{ success: boolean; user: User; error?: string }> => {
    const response = await api.put("/api/auth/profile", updateData);
    return response.data;
  },
};

export const documentsAPI = {
  getDocuments: async (): Promise<Document[]> => {
    const response = await api.get("/api/documents");
    return response.data;
  },

  getDocument: async (id: string): Promise<Document> => {
    const response = await api.get(`/api/documents/${id}`);
    return response.data;
  },

  uploadDocument: async (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/api/documents/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  deleteDocument: async (id: string): Promise<void> => {
    await api.delete(`/api/documents/${id}`);
  },

  checkPlagiarism: async (id: string): Promise<Document> => {
    const response = await api.post(`/api/documents/${id}/check`);
    return response.data;
  },
};

export default api;
