import React from "react";
import { useAuth } from "../../hooks/useAuth"; // Fixed import path
import { useDocuments } from "../../hooks/useDocuments";
import DocumentList from "../Documents/DocumentList";
import DocumentUpload from "../Documents/DocumentUpload";

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { documents, loading, error, uploadDocument, refreshDocuments } =
    useDocuments();

  const handleUpload = async (file: File) => {
    await uploadDocument(file);
    refreshDocuments();
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-4 py-5 sm:px-6">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-1 text-sm text-gray-500">
              Welcome back, {user?.name}
            </p>
          </div>
        </div>

        {/* Upload Section */}
        <div className="mt-6">
          <DocumentUpload onUpload={handleUpload} />
        </div>

        {/* Documents List */}
        <div className="mt-6">
          <DocumentList documents={documents} loading={loading} error={error} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
