import LandingPageSections from "../features/landing_content/components/LandingPageSections";
import RegisterButton from "../features/landing_content/components/RegisterButton";

export default function LandingPage() {

  return (
    <div className="relative min-h-screen  text-neutral-900 overflow-hidden">
      
      {/* Background Layers */}
      <div className="absolute inset-0 -z-20 bg-linear-to-b from-amber-100/50 via-stone-50 to-stone-50" />
      <div className="absolute -top-37.5 -left-37.5 w-150 h-150 bg-violet-300/20 rounded-full blur-3xl -z-10" />
      <div className="absolute -bottom-50 -right-50 w-175 h-175 bg-rose-200/30 rounded-full blur-3xl -z-10" />

      {/* Hero */}
      <section className="px-6 pt-16 pb-10 max-w-4xl mx-auto text-center">
        <h2 className="text-4xl sm:text-5xl md:text-6xl font-semibold leading-tight tracking-tight">
           Find the Right Book
        </h2>

        <p className="mt-8 text-lg sm:text-xl text-neutral-700 leading-relaxed">
            Upload a photo of a bookshelf and get instant recommendations based on your reading history.
        </p>

        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-5">
      <RegisterButton/>
        </div>
      </section>


      <LandingPageSections/>
    </div>
  );
}