import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import { tokenUtils } from '../../utils/tokenUtils';

const Navbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    try {
      // Get tokens from localStorage
      const accessToken = tokenUtils.getToken();
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!accessToken || !refreshToken) {
        console.warn('No tokens found, performing client-side logout only');
        performClientSideLogout();
        return;
      }

      // Call logout API
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/users/logout/`, {
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
    // Clear all tokens using centralized utility
    tokenUtils.clearAllTokens();
    
    // Update login state
    setIsLoggedIn(false);
    
    // Navigate to login page
    navigate('/login');
    
    console.log('✅ Admin logged out successfully');
  };



  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="navbar">
      <h1 className="logo">MITS Canteen Admin</h1>
      
      {/* Hamburger Menu for Mobile */}
      <div className="hamburger" onClick={toggleMobileMenu}>
        <span></span>
        <span></span>
        <span></span>
      </div>
      
      <div className={`nav-links ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
        {!isLoggedIn ? (
          <>
            <Link to="/login" className="nav-btn" onClick={() => setIsMobileMenuOpen(false)}>Login</Link>
          </>
        ) : (
          <button 
            onClick={() => {
              handleLogout();
              setIsMobileMenuOpen(false);
            }} 
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