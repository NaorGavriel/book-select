import InfoSection from "../../../components/ui/InfoSection"

export default function LandingPageSections() {
    return (
        <section>
            
            <InfoSection
            title="Add Your Favorite Books"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            background="bg-neutral-800"
            isDark
            media={
                <div className="w-full h-full bg-neutral-800 flex items-center justify-center shadow-sm">
                Account Preview
                </div>
            }
            />
            
            <InfoSection
            title="Upload a Picture of Books"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            background="bg-gradient-to-b from-white via-stone-50 to-amber-50"
            reverse
            media={
                <div className="w-full h-full bg-white flex items-center justify-center text-neutral-200">
                Add Book Preview
                </div>
            }
            />

            <InfoSection
            title="View Tailor Made Suggestions"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            background="bg-neutral-800"
            isDark
            media={
                <div className="w-full h-full bg-neutral-800 flex items-center justify-center shadow-sm">
                Upload Preview
                </div>
            }
            />
        </section>
       
    )
}