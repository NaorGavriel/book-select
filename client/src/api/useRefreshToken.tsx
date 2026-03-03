import api from "./axiosPublic";
import { useAuth } from "../features/authentication/AuthContext";


const useRefreshToken = () => {
    const { setAccessToken} = useAuth();

    const refresh = async () => {
        const response = await api.post('/refresh');
        const newAccessToken = response.data.access_token
        setAccessToken(newAccessToken)
        return newAccessToken;
    }

    return refresh;
}

export default useRefreshToken