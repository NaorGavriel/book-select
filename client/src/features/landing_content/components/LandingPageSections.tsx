import InfoSection from "../../../components/ui/InfoSection"
import  BookShelfSvg from "../../../assets/undraw_bookshelves_vhu6.svg"
import NewsFeedSvg from "../../../assets/undraw_newsfeed_8ms9.svg"
import UploadImageSvg from "../../../assets/undraw_upload-image_tpmp.svg"
import ViewResultsSvg from "../../../assets/undraw_choose_5kz4.svg"
import MediaBlock from "../../../components/ui/MediaBlock"

export default function LandingPageSections() {
    return (
        <section>
            <InfoSection
            title="Add Your Favorite Books"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
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
            title="Upload a Picture of Books"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
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
            title="View Tailor Made Suggestions"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
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