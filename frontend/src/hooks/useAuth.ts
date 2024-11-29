import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import { User } from "../types";

interface UseAuthReturn {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, userData: User) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export const useAuth = (): UseAuthReturn => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  const { user, token, login, logout, isAuthenticated } = context;

  // Add an updateUser function to update user data without full login
  const updateUser = (userData: Partial<User>) => {
    if (!user) return;

    const updatedUser = {
      ...user,
      ...userData,
    };

    // Update local storage
    localStorage.setItem("user", JSON.stringify(updatedUser));

    // Update context (this will trigger a re-render)
    if (token) {
      login(token, updatedUser);
    }
  };

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    updateUser,
  };
};

// Optional: Add authentication status check utility
export const useAuthStatus = () => {
  const { isAuthenticated, user } = useAuth();
  return { isAuthenticated, isLoading: false, user };
};

// Optional: Add protected route guard utility
export const useAuthGuard = () => {
  const { isAuthenticated, user } = useAuth();

  return {
    isAuthenticated,
    user,
    requireAuth: () => {
      if (!isAuthenticated) {
        throw new Error("Authentication required");
      }
      return true;
    },
  };
};

export default useAuth;
