import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

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

// Add response interceptor to handle errors and caching
api.interceptors.response.use(
  (response) => {
    // Cache menu data for 5 minutes
    if (response.config.url?.includes('/api/menu/customer')) {
      const cacheKey = `menu_${response.config.url}`;
      const cacheData = {
        data: response.data,
        timestamp: Date.now()
      };
      localStorage.setItem(cacheKey, JSON.stringify(cacheData));
    }
    return response;
  },
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

// Cache helper function
api.getCached = async (url, maxAge = 300000) => { // 5 minutes default
  const cacheKey = `menu_${url}`;
  const cached = localStorage.getItem(cacheKey);
  
  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < maxAge) {
      return { data };
    }
  }
  
  return api.get(url);
};

// Keep backend alive
setInterval(() => {
  api.get('/api/menu/customer/').catch(() => {});
}, 300000); // Ping every 5 minutes

export default api;