import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <Link to="/addmenu">Add Menu</Link>
      <Link to="/listitems">List Items</Link>
      <Link to="/orders">Orders</Link>
    </div>
  );
};

export default Sidebar;
