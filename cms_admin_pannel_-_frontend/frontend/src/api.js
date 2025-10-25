import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

api.interceptors.request.use((config) => {
  const userToken = localStorage.getItem("user-token");
  const adminToken = localStorage.getItem("admin-token");
  const accessToken = localStorage.getItem("access_token");

  // Check for different token types
  if (adminToken) {
    config.headers.Authorization = `Token ${adminToken}`;
  } else if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
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
      localStorage.removeItem('admin-token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      console.log('Authentication failed - tokens cleared');
    }
    return Promise.reject(error);
  }
);

export default api;