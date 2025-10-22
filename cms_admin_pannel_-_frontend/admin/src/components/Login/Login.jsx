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
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/users/simple-admin-login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          username: credentials.username,
          password: credentials.password,
        }),
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      const data = await response.json();
      console.log('Login response data:', data);

      if (response.ok) {
        // Store the hardcoded admin token
        const adminToken = 'admin-token-12345';
        console.log('Storing admin token:', adminToken);
        
        // Clear any existing tokens first
        localStorage.clear();
        
        // Store tokens with multiple keys for compatibility
        localStorage.setItem('admin_access_token', adminToken);
        localStorage.setItem('access_token', adminToken);
        localStorage.setItem('adminToken', adminToken);
        localStorage.setItem('user_type', 'admin');
        localStorage.setItem('isAdminLoggedIn', 'true');
        localStorage.setItem('user_data', JSON.stringify({
          username: 'canteen',
          first_name: 'Admin',
          last_name: 'User'
        }));

        // Set logged in state
        setIsLoggedIn(true);
        
        // Verify token was stored
        setTimeout(() => {
          const storedToken = localStorage.getItem('admin_access_token');
          console.log('Verification - stored token:', storedToken);
          console.log('All localStorage keys:', Object.keys(localStorage));
        }, 100);
        
        alert('✅ Login successful! Welcome Admin User');
      } else {
        // Handle error response
        if (data.error) {
          setError(data.error);
        } else if (data.non_field_errors) {
          setError(data.non_field_errors[0]);
        } else if (data.detail) {
          setError(data.detail);
        } else {
          setError('Invalid credentials. Please try again.');
        }
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Admin Login</h2>
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