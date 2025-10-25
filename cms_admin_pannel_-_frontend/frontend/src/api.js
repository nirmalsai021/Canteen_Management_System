import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

api.interceptors.request.use((config) => {
  const userToken = localStorage.getItem("user-token");
  const adminToken = localStorage.getItem("admin-token");

  // Admin token takes precedence if both exist
  if (adminToken) {
    config.headers.Authorization = `Token ${adminToken}`;
  } else if (userToken) {
    config.headers.Authorization = `Token ${userToken}`;
  }
  return config;
});

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('user-token');
      localStorage.removeItem('user');
      console.log('Authentication failed - tokens cleared');
    }
    return Promise.reject(error);
  }
);

export default api;
