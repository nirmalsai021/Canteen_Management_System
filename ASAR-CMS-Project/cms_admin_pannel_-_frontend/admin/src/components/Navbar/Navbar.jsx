import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    try {
      // Get tokens from localStorage
      const accessToken = localStorage.getItem('admin_access_token') || localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!accessToken || !refreshToken) {
        console.warn('No tokens found, performing client-side logout only');
        performClientSideLogout();
        return;
      }

      // Call logout API
      const response = await fetch('http://localhost:8000/api/users/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Logout successful:', data.message);
        performClientSideLogout();
      } else {
        // Even if API call fails, perform client-side logout
        console.error('Logout API failed, but continuing with client-side logout');
        const errorData = await response.json().catch(() => ({}));
        console.error('Error details:', errorData);
        performClientSideLogout();
      }
    } catch (error) {
      // Network error or other issues - still perform client-side logout
      console.error('Logout error:', error);
      performClientSideLogout();
    } finally {
      setIsLoggingOut(false);
    }
  };

  const performClientSideLogout = () => {
    // Clear all stored data
    localStorage.removeItem('admin_access_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    localStorage.removeItem('user_type');
    localStorage.removeItem('admin_profile');
    
    // Update login state
    setIsLoggedIn(false);
    
    // Navigate to login page
    navigate('/login');
    
    // Optional: reload to reset everything
    window.location.reload();
  };



  return (
    <nav className="navbar">
      <h1 className="logo">MITS Canteen Admin Panel</h1>
      <div className="nav-links">
        {!isLoggedIn ? (
          <>
            <Link to="/login" className="nav-btn">Login</Link>
            <Link to="/register" className="nav-btn">Register</Link>
          </>
        ) : (
          <button 
            onClick={handleLogout} 
            className="logout-button"
            disabled={isLoggingOut}
          >
            {isLoggingOut ? 'Logging out...' : 'Logout'}
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;