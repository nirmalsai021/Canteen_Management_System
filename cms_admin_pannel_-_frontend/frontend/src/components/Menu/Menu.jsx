import React, { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Menu.css';

// ✅ Import category images
import indianBreakfast from './Indian-Breakfast.jpg';
import easyLunch from './easy.jpg';
import drinks from './drinks.jpeg';
import snacks from './snacks.jpg';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ✅ Helper to read search query
const useQuery = () => new URLSearchParams(useLocation().search);

const Menu = ({ cart = {}, fetchCart, addToCart, removeFromCart }) => {
  const { filter } = useParams();
  const query = useQuery();
  const searchTerm = query.get('search') || '';
  const navigate = useNavigate();

  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ✅ Mapping frontend filters to backend categories
  const categoryMap = {
    'Indian-Breakfast': 'breakfast',
    'easy': 'lunch',
    'drinks': 'drinks',
    'snacks': 'snacks',
  };

  // ✅ Fetch menu items from backend
  const fetchMenuItems = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = {};

      // 🔧 Map the frontend filter to backend category
      if (filter) {
        const backendCategory = categoryMap[filter];
        if (backendCategory) {
          params.category = backendCategory;
        }
      }

      if (searchTerm) {
        params.q = searchTerm;
      }

      const url =
        searchTerm || filter
          ? `${API_BASE}/api/menu/customer/search/`
          : `${API_BASE}/api/menu/customer/`;

      const response = await axios.get(url, { params });

      setMenuItems(response.data);
    } catch (err) {
      console.error('❌ Error fetching menu:', err);
      setError('Failed to load menu items.');
    } finally {
      setLoading(false);
    }
  };

  // ✅ Add to cart
  const handleAdd = async (item) => {
    try {
      await addToCart(item);
      await fetchCart();
    } catch (err) {
      console.error('❌ Failed to add item:', err);
    }
  };

  // ✅ Remove from cart
  const handleRemove = async (item) => {
    try {
      await removeFromCart(item);
      await fetchCart();
    } catch (err) {
      console.error('❌ Failed to remove item:', err);
    }
  };

  useEffect(() => {
    fetchMenuItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter, searchTerm]);

  return (
    <div className="menu-container">
      {/* ✅ Category Filter Section */}
      <div className="menu-categories">
        <div className="category-card" onClick={() => navigate('/Menu/Indian-Breakfast')}>
          <img src={indianBreakfast} alt="Breakfast" />
          <p>Breakfast</p>
        </div>
        <div className="category-card" onClick={() => navigate('/Menu/easy')}>
          <img src={easyLunch} alt="Lunch" />
          <p>Lunch</p>
        </div>
        <div className="category-card" onClick={() => navigate('/Menu/drinks')}>
          <img src={drinks} alt="Drinks" />
          <p>Drinks</p>
        </div>
        <div className="category-card" onClick={() => navigate('/Menu/snacks')}>
          <img src={snacks} alt="Snacks" />
          <p>Snacks</p>
        </div>
      </div>

      {/* ✅ Menu Items Section */}
      {loading ? (
        <p style={{ textAlign: 'center' }}>Loading menu...</p>
      ) : error ? (
        <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>
      ) : (
        <div className="food-grid">
          {menuItems.length > 0 ? (
            menuItems.map((item) => (
              <div key={item.id} className="food-card">
                <img
                  src={item.image ? (item.image.startsWith('http') ? item.image : `${API_BASE}${item.image}`) : '/no-image.svg'}
                  alt={item.name}
                  className="food-image"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/no-image.svg';
                  }}
                  onLoad={() => console.log('Image loaded:', item.image)}
                />
                <h3>{item.name}</h3>
                <p>₹{parseFloat(item.price || 0).toFixed(2)}</p>
                <div className="cart-controls">
                  {cart[item.id] ? (
                    <>
                      <button className="qty-btn" onClick={() => handleRemove(item)}>-</button>
                      <span>{cart[item.id].quantity}</span>
                      <button className="qty-btn" onClick={() => handleAdd(item)}>+</button>
                    </>
                  ) : (
                    <button className="add-button" onClick={() => handleAdd(item)}>
                      Add to Cart
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p style={{ textAlign: 'center', fontSize: '18px', color: '#555' }}>
              No matching items found.
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default Menu;
