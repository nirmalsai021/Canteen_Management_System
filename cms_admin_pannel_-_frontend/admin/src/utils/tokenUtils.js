// Token management utility for admin panel
const TOKEN_KEY = 'adminToken';

export const tokenUtils = {
  // Get admin token
  getToken: () => {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Set admin token
  setToken: (token) => {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    }
  },

  // Remove admin token
  removeToken: () => {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Check if token exists
  hasToken: () => {
    return !!localStorage.getItem(TOKEN_KEY);
  },

  // Clear all possible token keys (for clean logout)
  clearAllTokens: () => {
    const keysToRemove = [
      'adminToken',
      'admin_access_token', 
      'access_token',
      'refresh_token'
    ];
    
    keysToRemove.forEach(key => {
      localStorage.removeItem(key);
    });
  }
};