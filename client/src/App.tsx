import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import usePersistentLogin from "./auth/usePersistentLogin";
import RequireAuth from "./auth/RequireAuth";
import LoginPage from "./pages/login";
import RegisterPage from "./pages/register";
import HomePage from "./pages/home";
import UploadPage from "./pages/upload";
import RecommendationsPage from "./pages/recommendations";
import ReadingHistoryPage from "./pages/readingHistory";

function AppContent() {
  const loading = usePersistentLogin();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected routes */}
      <Route element={<RequireAuth />}>
        <Route path="/home" element={<HomePage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/reading-history" element={<ReadingHistoryPage />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}