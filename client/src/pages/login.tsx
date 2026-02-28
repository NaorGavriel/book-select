import AuthCard from "../features/authentication/components/ui/AuthCard";
import LoginForm from "../features/authentication/components/LoginForm";
import AuthHeader from "../features/authentication/components/ui/AuthHeader";
  /**
  * LoginPage
  * ---------
  * Authenticates the user and initializes the session.
  * Sends credentials to /token, access token saved in memory inside AuthContext
  * refresh token stored as cookie
  */
export default function LoginPage() {
  return (
    <div className="relative min-h-[calc(100vh-140px)] flex items-center justify-center px-6">

      {/* Background Gradient */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-white via-violet-50 to-amber-100" />

      <div className="w-full max-w-md">
        <AuthHeader
          title="Welcome back"
          subtitle=""
        />

        <AuthCard>
          <LoginForm />
        </AuthCard>
      </div>

    </div>
  );  
}