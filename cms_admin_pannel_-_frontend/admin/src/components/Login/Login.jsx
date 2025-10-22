import React, { useState } from 'react';
import './Login.css';

const Login = ({ setIsLoggedIn }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Simple hardcoded admin login
    if (credentials.username === 'canteen' && credentials.password === 'canteen@321') {
      try {
        // Store admin token persistently
        const adminToken = 'admin-token-12345';
        
        // Clear localStorage first
        localStorage.clear();
        
        // Store with consistent key
        localStorage.setItem('ADMIN_TOKEN', adminToken);
        localStorage.setItem('ADMIN_LOGGED_IN', 'true');
        localStorage.setItem('ADMIN_USER', JSON.stringify({
          username: 'canteen',
          role: 'admin'
        }));
        
        console.log('✅ Admin token stored:', adminToken);
        
        // Set logged in state
        setIsLoggedIn(true);
        
        alert('✅ Login successful! Welcome Admin');
      } catch (err) {
        console.error('Storage error:', err);
        setError('Failed to store login data');
      }
    } else {
      setError('Invalid credentials. Use: canteen / canteen@321');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="form-container">
      <h2>Admin Login</h2>
      <div style={{marginBottom: '10px', fontSize: '14px', color: '#666'}}>
        Username: canteen | Password: canteen@321
      </div>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          name="username"
          value={credentials.username}
          onChange={handleChange}
          required
          disabled={isLoading}
        />
        <input
          type="password"
          placeholder="Password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          required
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;