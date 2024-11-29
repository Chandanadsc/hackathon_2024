import { useState, useEffect } from "react";
import { documentsAPI } from "../services/api";
import { Document } from "../types";

export const useDocuments = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const data = await documentsAPI.getDocuments();
      setDocuments(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch documents");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const uploadDocument = async (file: File) => {
    try {
      const newDocument = await documentsAPI.uploadDocument(file);
      setDocuments((prev) => [...prev, newDocument]);
      return newDocument;
    } catch (err: any) {
      throw new Error(err.message || "Failed to upload document");
    }
  };

  return {
    documents,
    loading,
    error,
    uploadDocument,
    refreshDocuments: fetchDocuments,
  };
};
