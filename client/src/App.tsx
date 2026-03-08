import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./features/authentication/AuthContext";
import RequireAuth from "./features/authentication/RequireAuth";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegistrationPage";
import HomePage from "./pages/HomePage";
import ResultsPage from "./pages/ResultsPage";
import RecommendationsPage from "./pages/RecommendationsPage";
import ReadingHistoryPage from "./pages/ReadingHistoryPage";
import UploadPage from "./pages/UploadPage";
import LandingPage from "./pages/LandingPage";
import Layout from "./components/ui/Layout";
import LoginButton from "./features/landing_content/components/LoginButton";
import LogoutButton from "./features/authentication/components/LogoutButton";
import PersistLogin from "./features/authentication/components/PersistLogin";
import RateLimitPopup from "./components/RateLimitPopup";


function AppContent() {
  return (
    <Routes>
      {/* Landing Page Layout */}
      <Route element={<Layout headerRight={<LoginButton />} />}>
        <Route path="/" element={<LandingPage />} />
      </Route>

      {/* Public Auth Pages */}
      <Route element={<Layout/>}>
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      <Route element= {<PersistLogin/>}>
        <Route element={<Layout/>}>
          <Route path="/login" element={<LoginPage />} />
        </Route>
      </Route>
      

      {/* Protected Pages */}
      <Route element={<PersistLogin/>}>
        <Route element={<RequireAuth />}>
          <Route element={<Layout headerRight={<LogoutButton/>}/>}>
            <Route path="/home" element={<HomePage />} />
            <Route path="/results/:jobId" element={<ResultsPage />} />
            <Route path="/recommendations" element={<RecommendationsPage />} />
            <Route path="/reading-history" element={<ReadingHistoryPage />} />
            <Route path="/upload" element={<UploadPage />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
      <AuthProvider>
        <BrowserRouter>
          <RateLimitPopup/>
          <AppContent />
        </BrowserRouter>
      </AuthProvider>
    
  );
}