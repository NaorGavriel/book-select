import { useEffect } from "react";
import api from "./axiosPrivate";
import { useAuth } from "../features/authentication/AuthContext";
import useRefreshToken from "./useRefreshToken";


export default function useApi() {
  const { accessToken, setAccessToken } = useAuth();
  const refresh = useRefreshToken();
 
  useEffect(() => {
    // Request interceptor
    const requestInterceptor = api.interceptors.request.use((config) => {
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      return config;
    });

    // Runs when a response is received. if successful, return it. if 401 (Unauthorized), try to refresh token.
    const responseInterceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        const status = error.response?.status;

        // Handle rate limit
        if (status === 429) {
          window.dispatchEvent(new Event("rate-limit"));
          return Promise.reject(error);
        }

        // If access token expired
        if (status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newAccessToken = await refresh();
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return api(originalRequest); // retry original request
          } catch (refreshError) {
            setAccessToken(null);
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(requestInterceptor);
      api.interceptors.response.eject(responseInterceptor);
    };
  }, [accessToken, refresh]);

  return api;
}