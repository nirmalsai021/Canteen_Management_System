import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

api.interceptors.request.use((config) => {
  // Get admin token (stored as 'admin-token')
  const adminToken = localStorage.getItem("admin-token");

  if (adminToken) {
    config.headers.Authorization = `Token ${adminToken}`;
    console.log('🔑 Using admin token');
  } else {
    console.log('⚠️ No admin token found');
  }
  return config;
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.log('❌ 401 Unauthorized - clearing admin token');
      localStorage.removeItem('admin-token');
      // Don't redirect here, let components handle it
    }
    return Promise.reject(error);
  }
);

export default api;
