import {useState} from 'react'
import useAxios from '../../api/useAxios';
import { useNavigate } from 'react-router';

/**
 * UploadImage
 * -----------
 * Allows the user to upload an image of a bookshelf and create a processing job.
 *
 * - File is sent to POST /jobs
 * - On success will navigate to /results
 */
function UploadImage() {
    const api = useAxios();
    const navigate = useNavigate();

    const [image, setImage] = useState<File | null>(null); // Selected image file (null until user chooses a file)

    /**
     * Handles file selection from input.
     * Stores the first selected file in state.
     */
    const handleImageChange = (event : React.ChangeEvent<HTMLInputElement>) => {
        const imageFile = event.target.files?.[0];
        if (imageFile) {
            setImage(imageFile);
        }
    }

    /**
     * Sends the selected image to the backend.
     * Creates multipart/form-data request and navigates to results on success.
     */
    const handleSubmit = async () => {
    
        if (!image) return;

        try {
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
        }
    };

    return (
        <>
            <div><h2>Upload image of books</h2></div>
            <div>
                <input type="file" accept="image/*" onChange={handleImageChange}/>
            </div>
            <button type="submit" onClick={handleSubmit}>Upload</button>
        </>


    )
    
}

export default UploadImage