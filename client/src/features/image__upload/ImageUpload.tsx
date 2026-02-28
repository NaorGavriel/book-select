import {useState} from 'react'
import useAxios from '../../api/useAxios';
import { useNavigate } from 'react-router';
import ImageUploadHeader from './components/ImageUploadHeader';
/**
 * ImageUpload
 * -----------
 * Allows the user to upload an image of a bookshelf and create a processing job.
 *
 * - File is sent to POST /jobs
 * - On success will navigate to /results
 */
function ImageUpload() {
    const api = useAxios();
    const navigate = useNavigate();

    const [image, setImage] = useState<File | null>(null); // Selected image file (null until user chooses a file)
    const [preview, setPreview] = useState<string | null>(null);
    const [uploading, setUploading] = useState(false);

    /**
     * Handles file selection from input.
     * Stores the first selected file in state.
     */
    const handleImageChange = (event : React.ChangeEvent<HTMLInputElement>) => {
        const imageFile = event.target.files?.[0];
        if (imageFile) {
            setImage(imageFile);
            setPreview(URL.createObjectURL(imageFile));
        }
    }

    /**
     * Sends the selected image to the backend.
     * Creates multipart/form-data request and navigates to results on success.
     */
    const handleSubmit = async () => {
    
        if (!image) return;

        try {
            setUploading(true);
            const formData = new FormData();
            formData.append("file", image);

            const response = await api.post("/jobs", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            });
            
            const { job_id } = response.data; // extracting job_id from response
            navigate(`/results/${job_id}`);
        } catch {
            console.error("Upload failed");
        } finally {
            setUploading(false);
        }
    };

    return (
    <div className="bg-white border border-neutral-200 shadow-xl rounded-2xl p-10">

      <ImageUploadHeader/>

      {/* Upload Area */}
      <div className="flex flex-col items-center">

        <label className="w-full cursor-pointer">
          <div className="flex flex-col items-center justify-center 
                          border-2 border-dashed border-neutral-300 
                          rounded-xl p-10 bg-neutral-50 
                          hover:border-neutral-400 hover:bg-neutral-100 
                          transition text-center">

            {preview ? (
              <img
                src={preview}
                alt="Preview"
                className="max-h-64 rounded-lg shadow-md mb-4"
              />
            ) : (
              <>
                <p className="text-neutral-600 font-medium">
                  Click to select an image
                </p>
                <p className="text-neutral-400 text-sm mt-1">
                  JPG, PNG supported
                </p>
              </>
            )}
          </div>

          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="hidden"
          />
        </label>

        {/* Upload Button */}
        <button
          onClick={handleSubmit}
          disabled={!image || uploading}
          className="mt-8 px-6 py-3 rounded-lg bg-neutral-800 text-white 
                     font-medium hover:bg-neutral-700 transition 
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploading ? "Uploading..." : "Analyze Books"}
        </button>
      </div>
    </div>
  );
    
}

export default ImageUpload