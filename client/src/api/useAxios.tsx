import { useEffect } from "react";
import api from "./axios";
import { useAuth } from "../auth/AuthContext";

export default function useAxios() {
  const { accessToken, setAccessToken } = useAuth();

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

        // If access token expired
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const response = await api.post("/refresh");
            const newAccessToken = response.data.access_token;

            setAccessToken(newAccessToken);

            // retry original request
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return api(originalRequest);
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
  }, [accessToken]);

  return api;
}