import InfoSection from "../../../components/ui/InfoSection"
import NewsFeedSvg from "../../../assets/undraw_newsfeed_8ms9.svg"
import UploadImageSvg from "../../../assets/undraw_upload-image_tpmp.svg"
import ViewResultsSvg from "../../../assets/undraw_choose_5kz4.svg"
import MediaBlock from "../../../components/ui/MediaBlock"

export default function LandingPageSections() {
    return (
        <section>
            <InfoSection
            title="Tell Us What You Like"
            description="Add books you’ve enjoyed so the system can understand your reading preferences."
            background="bg-neutral-800"
            isDark
            media={
                <MediaBlock
                src={NewsFeedSvg}
                alt="Upload books illustration"
                glowColor="bg-amber-100/25"
                align="center"
                />
            }
            />
            
            <InfoSection
            title="Take a Shelf Photo"
            description="Upload a photo of books from a shelf in a store, library, or anywhere you discover new titles."
            background="bg-gradient-to-b from-white via-stone-50 to-amber-50"
            reverse
            media={
                <MediaBlock
                src={UploadImageSvg}
                alt="Upload books illustration"
                glowColor="bg-amber-100/25"
                align="center"
                />
            }
            />

            <InfoSection
            title="Get Smart Recommendations"
            description="See which books are a Good Match, Maybe, or Avoid based on your reading history."
            background="bg-neutral-800"
            isDark
            media={
                <MediaBlock
                src={ViewResultsSvg}
                alt="Upload books illustration"
                glowColor="bg-amber-100/25"
                align="center"
                />
            }
            />
        </section>
       
    )
}