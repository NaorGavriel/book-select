import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-screen bg-stone-50 text-neutral-900 overflow-hidden">

      {/* Background Layers */}
      <div className="absolute inset-0 -z-20 bg-gradient-to-b from-amber-100/50 via-stone-50 to-stone-50" />
      <div className="absolute top-[-150px] left-[-150px] w-[600px] h-[600px] bg-emerald-200/30 rounded-full blur-3xl -z-10" />
      <div className="absolute bottom-[-200px] right-[-200px] w-[700px] h-[700px] bg-rose-200/30 rounded-full blur-3xl -z-10" />

      {/* Logo */}
      <div className="px-6 py-6 max-w-7xl mx-auto">
        <h1 className="text-2xl font-semibold tracking-tight">
          BookSelect
        </h1>
      </div>

      {/* Hero */}
      <section className="px-6 pt-16 pb-10 max-w-4xl mx-auto text-center">
        <h2 className="text-4xl sm:text-5xl md:text-6xl font-semibold leading-tight tracking-tight">
          Discover books that feel like home.
        </h2>

        <p className="mt-8 text-lg sm:text-xl text-neutral-700 leading-relaxed">
          Thoughtful recommendations, beautifully presented.
          A calm, focused space for readers who care about what they read next.
        </p>

        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            onClick={() => navigate("/register")}
            className="px-8 py-3 text-base font-medium rounded-full 
                       bg-emerald-600 text-white
                       hover:bg-emerald-700 transition shadow-sm"
          >
            Get Started
          </button>

          <button
            onClick={() => navigate("/login")}
            className="px-8 py-3 text-base font-medium rounded-full 
                       border border-neutral-300 bg-white/70
                       hover:bg-white transition"
          >
            Login
          </button>
        </div>
      </section>

{/* Instruction Cards */}
<section className="px-6 mt-24 pb-40">
  <div className="max-w-6xl mx-auto flex flex-col gap-32">

    {/* Card 1 */}
    <div className="rounded-3xl overflow-hidden shadow-xl border border-emerald-200
                    bg-gradient-to-br from-emerald-100 to-emerald-50">
      
      <div className="flex flex-col lg:flex-row">

        {/* Text */}
        <div className="p-14 lg:w-1/2 flex flex-col justify-center">
          <h3 className="text-4xl font-semibold mb-8 text-emerald-800">
            1. Create Your Account
          </h3>
          <p className="text-xl text-emerald-900/80 leading-relaxed">
            Login or create your account using the buttons above
            to begin your personalized reading journey.
          </p>
        </div>

        {/* Media */}
        <div className="lg:w-1/2 bg-white/60 flex items-center justify-center 
                        min-h-[300px] lg:min-h-[400px]">
          <span className="text-emerald-700 text-lg font-medium">
            Image / Media Preview
          </span>
        </div>

      </div>
    </div>

    {/* Card 2 */}
    <div className="rounded-3xl overflow-hidden shadow-xl border border-amber-200
                    bg-gradient-to-br from-amber-100 to-amber-50">
      
      <div className="flex flex-col lg:flex-row">

        <div className="p-14 lg:w-1/2 flex flex-col justify-center">
          <h3 className="text-4xl font-semibold mb-8 text-amber-800">
            2. Add Your Favorite Books
          </h3>
          <p className="text-xl text-amber-900/80 leading-relaxed">
            Use the Add Book button to tell us what you love.
            The more we understand your taste, the better your
            recommendations become.
          </p>
        </div>

        <div className="lg:w-1/2 bg-white/60 flex items-center justify-center 
                        min-h-[300px] lg:min-h-[400px]">
          <span className="text-amber-700 text-lg font-medium">
            Image / Media Preview
          </span>
        </div>

      </div>
    </div>

    {/* Card 3 */}
    <div className="rounded-3xl overflow-hidden shadow-xl border border-sky-200
                    bg-gradient-to-br from-sky-100 to-sky-50">
      
      <div className="flex flex-col lg:flex-row">

        <div className="p-14 lg:w-1/2 flex flex-col justify-center">
          <h3 className="text-4xl font-semibold mb-8 text-sky-800">
            3. Upload Books You’re Considering
          </h3>
          <p className="text-xl text-sky-900/80 leading-relaxed">
            Upload an image of books you're thinking about
            and receive tailored recommendations based on
            your unique preferences.
          </p>
        </div>

        <div className="lg:w-1/2 bg-white/60 flex items-center justify-center 
                        min-h-[300px] lg:min-h-[400px]">
          <span className="text-sky-700 text-lg font-medium">
            Image / Media Preview
          </span>
        </div>

      </div>
    </div>

    {/* Card 4 */}
    <div className="rounded-3xl overflow-hidden shadow-xl border border-rose-200
                    bg-gradient-to-br from-rose-100 to-rose-50">
      
      <div className="flex flex-col lg:flex-row">

        <div className="p-14 lg:w-1/2 flex flex-col justify-center">
          <h3 className="text-4xl font-semibold mb-8 text-rose-800">
            4. Access Your History
          </h3>
          <p className="text-xl text-rose-900/80 leading-relaxed">
            Access your past recommendations anytime using
            the History button and track your reading evolution.
          </p>
        </div>

        <div className="lg:w-1/2 bg-white/60 flex items-center justify-center 
                        min-h-[300px] lg:min-h-[400px]">
          <span className="text-rose-700 text-lg font-medium">
            Image / Media Preview
          </span>
        </div>

      </div>
    </div>

  </div>
</section>

    </div>
  );
}