import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

api.interceptors.request.use((config) => {
  // Try different token sources in order
  const tokens = [
    localStorage.getItem("admin-token"),
    localStorage.getItem("user-token"), 
    localStorage.getItem("access_token")
  ];
  
  const token = tokens.find(t => t && t !== 'null' && t !== 'undefined');
  
  if (token) {
    // Use Token auth for admin/user tokens, Bearer for JWT
    if (token.includes('.')) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      config.headers.Authorization = `Token ${token}`;
    }
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