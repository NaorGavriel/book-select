import AuthHeader from "../features/authentication/components/ui/AuthHeader";
import AuthCard from "../features/authentication/components/ui/AuthCard";
import RegisterForm from "../features/authentication/components/RegisterForm";

export default function RegisterPage() {
  return (
    <div className="relative min-h-[calc(100vh-140px)] flex items-center justify-center px-6">

      {/* Background Gradient */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-white via-stone-50 to-emerald-50" />

      <div className="w-full max-w-md">
        <AuthHeader
          title="Create your account"
          subtitle="Start your personalized reading journey."
        />

        <AuthCard>
          <RegisterForm />
        </AuthCard>
      </div>

    </div>
  );
}