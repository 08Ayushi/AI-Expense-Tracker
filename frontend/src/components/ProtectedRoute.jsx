import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

// Wraps private pages: redirects to /login when not authenticated.
export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-brand" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
