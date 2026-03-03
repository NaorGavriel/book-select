import ImageUpload from "../features/image__upload/ImageUpload";
/**
 * UploadPage
 * --------------
 * Allows user to upload a picture of a books.
 */
export default function UploadPage() {
  return (
    <div className="min-h-[calc(100vh-140px)] bg-linear-to-b from-neutral-100 to-slate-100 px-6 py-16">
      <div className="max-w-2xl mx-auto">
        <ImageUpload />
      </div>
    </div>
  );
}