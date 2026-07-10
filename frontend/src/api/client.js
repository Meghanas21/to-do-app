import axios from "axios";

/**
 * Single shared axios instance.
 *
 * WHY THIS FIXES CORS/URL BUGS:
 * - baseURL comes from VITE_API_BASE_URL (an env var), never hardcoded as
 *   "http://localhost:8000" scattered across components. If the backend
 *   port or host ever changes, only .env needs to change.
 * - withCredentials is NOT enabled here because this app uses a Bearer
 *   token in the Authorization header (not cookies). Enabling
 *   withCredentials without the backend also allowing credentials +
 *   explicit origins is a common source of CORS failures, so we only
 *   turn it on if you actually switch to cookie-based auth.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach the JWT to every outgoing request if we have one.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Centralized error handling: normalize backend error shape and handle
// expired/invalid tokens by logging the user out.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Backend responded with an error status
      if (error.response.status === 401) {
        localStorage.removeItem("access_token");
      }
      const message = error.response.data?.detail || "Something went wrong. Please try again.";
      return Promise.reject(new Error(message));
    }
    if (error.request) {
      // Request was made but no response received — this is what a REAL
      // CORS block or network failure looks like from the browser's side.
      return Promise.reject(
        new Error(
          "Could not reach the server. Check your connection or that the backend is running."
        )
      );
    }
    return Promise.reject(error);
  }
);

export default apiClient;
