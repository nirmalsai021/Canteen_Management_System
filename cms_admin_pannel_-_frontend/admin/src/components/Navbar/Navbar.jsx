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
      // Get admin token from localStorage
      const accessToken = tokenUtils.getToken();
      
      if (!accessToken) {
        console.warn('No admin token found, performing client-side logout only');
        performClientSideLogout();
        return;
      }

      // For admin, just perform client-side logout (no API logout needed)
      console.log('Admin logout - performing client-side cleanup');
      performClientSideLogout();
      return;


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