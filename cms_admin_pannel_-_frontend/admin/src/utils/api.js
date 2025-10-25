import axios from 'axios';
import { tokenUtils } from './tokenUtils';

const BASE_URL = process.env.REACT_APP_API_URL || 'https://canteen-backend-bbqk.onrender.com';

const api = axios.create({
  baseURL: BASE_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = tokenUtils.getToken();
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenUtils.removeToken();
      console.log('Admin authentication failed - token cleared');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;