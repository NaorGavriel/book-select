import HomeButton from "../components/HomeButton";
import UploadImage from "../features/image__upload/ImageUpload";
/**
 * UploadPage
 * --------------
 * Allows user to upload a picture of a books.
 */
export default function UploadPage() {
  return (
    <div>
      <HomeButton />
      <UploadImage/>
    </div>
  );
}