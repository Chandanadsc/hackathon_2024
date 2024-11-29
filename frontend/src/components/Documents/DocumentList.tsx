import React from "react";
import { Document } from "../../types";

interface DocumentListProps {
  documents: Document[];
  loading: boolean;
  error: string | null;
}

const DocumentList: React.FC<DocumentListProps> = ({
  documents,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center h-48">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No documents uploaded yet.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {documents.map((doc) => (
          <li key={doc.id} className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {doc.filename}
                </h3>
                <p className="text-sm text-gray-500">
                  Uploaded on {new Date(doc.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="flex items-center">
                {doc.status === "processing" && (
                  <span className="px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                    Processing
                  </span>
                )}
                {doc.status === "completed" &&
                  doc.similarity_score !== undefined && (
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        doc.similarity_score > 0.7
                          ? "bg-red-100 text-red-800"
                          : doc.similarity_score > 0.4
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-green-100 text-green-800"
                      }`}>
                      {Math.round(doc.similarity_score * 100)}% Similar
                    </span>
                  )}
                {doc.status === "error" && (
                  <span className="px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                    Error
                  </span>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DocumentList;
