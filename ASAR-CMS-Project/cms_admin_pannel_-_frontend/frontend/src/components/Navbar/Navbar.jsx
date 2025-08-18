import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isLoggedIn, setIsLoggedIn, cart }) => {
  const [search, setSearch] = useState('');
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();
  const dropdownRef = useRef();

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (search.trim()) {
      navigate(`/menu?search=${encodeURIComponent(search.trim())}`);
    } else {
      navigate('/menu');
    }
  };

  const toggleDropdown = () => {
    setDropdownOpen((prev) => !prev);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    navigate('/');
  };

  const handleOrdersClick = () => {
    navigate('/orders');
  };

  const cartItemCount = Object.values(cart || {}).reduce(
    (count, item) => count + item.quantity,
    0
  );

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="logo">MITS Canteen</Link>
      </div>

      <div className="navbar-right">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/menu" className="nav-link">Menu</Link>
        <Link to="/cart" className="nav-link cart-icon-wrapper">
          <span className="cart-text">Cart</span>
          <span className="cart-icon" role="img" aria-label="cart">🛒</span>
          {cartItemCount > 0 && <span className="cart-dot" />}
        </Link>

        {isLoggedIn ? (
          <div className="profile-dropdown-wrapper" ref={dropdownRef}>
            <button className="profile-btn" onClick={toggleDropdown} title="Profile">
              👤
            </button>
            {dropdownOpen && (
              <div className="dropdown">
                <button onClick={() => navigate('/profile')} className="dropdown-link">My Profile</button>
                <button onClick={handleOrdersClick} className="dropdown-link">Orders</button>
                <button onClick={handleLogout} className="dropdown-link">Logout</button>
              </div>
            )}
          </div>
        ) : (
          <>
            <Link to="/register">
              <button className="btn">Sign Up</button>
            </Link>
            <Link to="/login">
              <button className="btn btn-outline">Log In</button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
