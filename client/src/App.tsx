import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./features/authentication/AuthContext";
import usePersistentLogin from "./features/authentication/hooks/usePersistentLogin";
import RequireAuth from "./features/authentication/RequireAuth";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import HomePage from "./pages/Home";
import ResultsPage from "./pages/Results";
import RecommendationsPage from "./pages/Recommendations";
import ReadingHistoryPage from "./pages/ReadingHistory";
import UploadPage from "./pages/Upload";
import LandingPage from "./pages/LandingPage";
import Layout from "./components/ui/Layout";
import LoginButton from "./features/landing_content/components/LoginButton";

function AppContent() {
  const loading = usePersistentLogin();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Routes>

      {/* Landing Page Layout */}
      <Route element={<Layout headerRight={<LoginButton />} />}>
        <Route path="/" element={<LandingPage />} />
      </Route>

      {/* Public Auth Pages */}
      <Route element={<Layout/>}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Protected Pages */}
      <Route element={<RequireAuth />}>
        <Route element={<Layout />}>
          <Route path="/home" element={<HomePage />} />
          <Route path="/results/:jobId" element={<ResultsPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/reading-history" element={<ReadingHistoryPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Route>
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