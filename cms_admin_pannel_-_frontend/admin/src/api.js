import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "https://canteen-backend-bbqk.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
});

// Add request timeout - longer for cold starts
api.defaults.timeout = 60000; // 60 seconds for Render cold start

import { tokenUtils } from './utils/tokenUtils';

api.interceptors.request.use((config) => {
  // Get admin token using centralized utility
  const adminToken = tokenUtils.getToken();
  
  if (adminToken) {
    config.headers.Authorization = `Token ${adminToken}`;
    console.log('🔑 Using admin token:', adminToken.substring(0, 10) + '...');
  } else {
    console.log('⚠️ No admin token found');
  }
  return config;
});

// Helper function to fix corrupted image URLs
const fixImageUrl = (url) => {
  if (!url) return null;
  
  // If URL is corrupted with media path, extract the real URL
  if (url.includes('/media/https%3A')) {
    const decodedUrl = decodeURIComponent(url.split('/media/')[1]);
    return decodedUrl;
  }
  
  return url;
};

// Add response interceptor to handle errors - NEVER CLEAR ADMIN TOKENS
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
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.log('🚫 401 Error - Admin tokens never expire, keeping token');
      // CRITICAL: Never clear admin tokens under any circumstances
    }
    return Promise.reject(error);
  }
);

export default api;
