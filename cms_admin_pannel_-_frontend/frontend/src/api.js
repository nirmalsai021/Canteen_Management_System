import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

api.interceptors.request.use((config) => {
  // Get JWT token first (for user authentication)
  const accessToken = localStorage.getItem("access_token");
  const adminToken = localStorage.getItem("admin-token");
  
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
    console.log('🔑 Using JWT Bearer token');
  } else if (adminToken) {
    config.headers.Authorization = `Token ${adminToken}`;
    console.log('🔑 Using admin token');
  } else {
    console.log('⚠️ No authentication token found');
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
      console.log('❌ 401 Unauthorized - clearing tokens');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      localStorage.removeItem('admin-token');
      // Don't redirect here, let components handle it
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