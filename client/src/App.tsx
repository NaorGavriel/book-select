import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import usePersistentLogin from "./auth/usePersistentLogin";
import RequireAuth from "./auth/RequireAuth";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import HomePage from "./pages/Home";
import ResultsPage from "./pages/Results";
import RecommendationsPage from "./pages/Recommendations";
import ReadingHistoryPage from "./pages/ReadingHistory";
import UploadPage from "./pages/Upload";

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
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/reading-history" element={<ReadingHistoryPage />} />
        <Route path="/upload" element={<UploadPage />} />
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