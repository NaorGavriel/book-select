import { createContext, useContext, useState } from "react";

/**
 *  AuthContext
 *  -----------
 *  Global authentication state.
 *  Holds the current access token in memory and exposes a setter.
 *  Access token gets cleared on page reload.
 */
type AuthContextType = {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider
 * ------------
 * Wraps the application and provides authentication state.
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(null);

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * useAuth
 * -------
 * Hook to access authentication state.
 * Throws if used outside <AuthProvider> to prevent undefined context usage.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  // checks that useAuth was used by a component that is within AuthProvider
  if (!context) throw new Error("useAuth must be used inside AuthProvider"); 
  return context;
}