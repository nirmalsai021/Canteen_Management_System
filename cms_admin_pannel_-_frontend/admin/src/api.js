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

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.log('❌ 401 Unauthorized - but keeping admin token for retry');
      // Don't clear admin token immediately, let user retry
    }
    return Promise.reject(error);
  }
);

export default api;
