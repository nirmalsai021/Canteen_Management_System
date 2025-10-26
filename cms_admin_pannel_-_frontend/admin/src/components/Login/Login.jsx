import React, { useState } from 'react';
import './Login.css';
import { tokenUtils } from '../../utils/tokenUtils';

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

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/users/simple-admin-login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Login response:', data);
        const token = data.access || data.token;
        tokenUtils.setToken(token);
        console.log('Token stored:', token);
        setIsLoggedIn(true);
        alert('✅ Login successful! Welcome Admin');
      } else {
        const errorData = await response.json().catch(() => ({}));
        setError(errorData.error || 'Invalid credentials. Use: canteen / canteen@321');
      }
    } catch (err) {
      setError('Network error. Please check your connection.');
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