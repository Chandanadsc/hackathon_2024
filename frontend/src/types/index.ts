export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Document {
  id: string;
  filename: string;
  created_at: string;
  similarity_score?: number;
  status: "processing" | "completed" | "error";
}

export interface AuthResponse {
  token: string;
  user: User;
}
