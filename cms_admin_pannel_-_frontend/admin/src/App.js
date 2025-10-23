import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { tokenUtils } from './utils/tokenUtils';

// Components
import Navbar from './components/Navbar/Navbar';
import Sidebar from './components/Sidebar/Sidebar';
import Login from './components/Login/Login';
import AddMenu from './components/AddMenu/AddMenu';
import ListItems from './components/ListItems/ListItems';
import Orders from './components/Orders/Orders';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return tokenUtils.hasToken();
  });
  const [menuItems, setMenuItems] = useState([]);

  // Monitor token changes to debug token loss
  useEffect(() => {
    const checkToken = () => {
      if (isLoggedIn && !tokenUtils.hasToken()) {
        setIsLoggedIn(false);
      }
    };

    // Check token every 5 seconds when logged in
    const interval = isLoggedIn ? setInterval(checkToken, 5000) : null;
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isLoggedIn]);

  // CRUD operations for menu
  const handleAddMenuItem = (item) => {
    setMenuItems([...menuItems, item]);
  };

  const handleUpdateMenuItem = (index, updatedItem) => {
    const updatedList = [...menuItems];
    updatedList[index] = updatedItem;
    setMenuItems(updatedList);
  };

  const handleDeleteMenuItem = (index) => {
    setMenuItems(menuItems.filter((_, i) => i !== index));
  };

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      
      <div className="app-container" style={{ display: 'flex' }}>
        {isLoggedIn && <Sidebar />}

        <div className="main-content" style={{ padding: '20px', flex: 1, marginLeft: isLoggedIn ? '160px' : '0' }}>
          <Routes>

            {/* Public Routes */}
            {!isLoggedIn && (
              <>
                <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
                <Route path="*" element={<Navigate to="/login" />} />
              </>
            )}

            {/* Protected Routes */}
            {isLoggedIn && (
              <>
                <Route path="/addmenu" element={<AddMenu onAddMenuItem={handleAddMenuItem} />} />
                <Route
                  path="/listitems"
                  element={
                    <ListItems
                      onUpdateMenuItem={handleUpdateMenuItem}
                      onDeleteMenuItem={handleDeleteMenuItem}
                    />
                  }
                />
                <Route path="/orders" element={<Orders />} />

                <Route path="*" element={<Navigate to="/addmenu" />} />
              </>
            )}

          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
