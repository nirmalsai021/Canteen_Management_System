import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

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

export default api;
