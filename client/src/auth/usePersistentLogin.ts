import { useEffect, useState } from "react";
import api from "../api/axios";
import { useAuth } from "./AuthContext";

/**
 * Runs once when the app loads.

 * - Try to get a new access token using the refresh cookie
 * - If cookie is valid : user stays logged in
 * - If not : user stays logged out
 *
 * Returns:
 *   loading = true while checking authentication
 */
export default function usePersistentLogin() {
    const { accessToken, setAccessToken } = useAuth();
    const [loading, setLoading] = useState(true);
    
    useEffect(() => { // useEffect runs when component finishes rendering
        console.log("PersistentLogin effect running");

        const verifyUser = async () => {
            // If we already have an access token, skip
            if (accessToken) {
            setLoading(false);
            return;
            }

            try {
            const response = await api.post("/refresh");

            const newAccessToken = response.data.access_token;

            // Save token in memory
            setAccessToken(newAccessToken);

            } catch (err) {
            // Refresh failed : user not logged in
            setAccessToken(null);
            } finally {
            setLoading(false);
            }
        };

    verifyUser();
    }, []);

    return loading;
}