import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

api.interceptors.request.use((config) => {
  // Get JWT token for customer authentication
  const accessToken = localStorage.getItem("access_token");
  
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
    console.log('🔑 Using JWT Bearer token');
  } else {
    console.log('⚠️ No access token found');
  }
  return config;
});

// Helper function to fix corrupted image URLs
const fixImageUrl = (url) => {
  if (!url) return null;
  
  // If URL is corrupted with media path, extract the real URL
  if (url.includes('/media/https%3A')) {
    let decodedUrl = decodeURIComponent(url.split('/media/')[1]);
    // Fix missing slash in https:/
    if (decodedUrl.startsWith('https:/') && !decodedUrl.startsWith('https://')) {
      decodedUrl = decodedUrl.replace('https:/', 'https://');
    }
    return decodedUrl;
  }
  
  return url;
};

// Add response interceptor to handle errors and caching
api.interceptors.response.use(
  (response) => {
    // Fix image URLs in menu responses
    if (response.config.url?.includes('/api/menu/')) {
      if (Array.isArray(response.data)) {
        response.data = response.data.map(item => ({
          ...item,
          image: fixImageUrl(item.image)
        }));
      } else if (response.data.image) {
        response.data.image = fixImageUrl(response.data.image);
      }
    }
    
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
      console.log('❌ 401 Unauthorized - clearing JWT tokens');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
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