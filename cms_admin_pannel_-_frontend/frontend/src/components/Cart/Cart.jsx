import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Cart.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Cart = ({ cart, setCart }) => {
  const [orderDetails, setOrderDetails] = useState(null);
  const [placingOrder, setPlacingOrder] = useState(false); // ✅ Added loader state
  const navigate = useNavigate();

  const token = localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user'));

  const axiosConfig = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const fetchCart = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/cart/`, axiosConfig);
      const data = res.data;
      console.log('📦 Fetched Cart Response:', data);

      const fetchedCart = {};
      const items = data.items ?? [];

      items.forEach((item) => {
        const menuItemId =
          typeof item.menu_item === 'object' ? item.menu_item.id : item.menu_item;

        const menuItemName = item.menu_item_name || item.menu_item?.name || `Item #${menuItemId}`;
        const menuItemPrice = parseFloat(item.menu_item_price || item.menu_item?.price || 0);

        fetchedCart[menuItemId] = {
          cart_item_id: item.id,
          id: menuItemId,
          name: menuItemName,
          price: menuItemPrice,
          quantity: item.quantity,
        };
      });

      setCart(fetchedCart);
      console.log('✅ Synced cart state:', fetchedCart);
    } catch (err) {
      console.error('❌ Failed to fetch cart:', err);
      setCart({});
    }
  };

  useEffect(() => {
    if (token) fetchCart();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleRemove = async (menuItemId) => {
    const cartItemId = cart[menuItemId]?.cart_item_id;
    if (!cartItemId) return;

    try {
      await axios.delete(`${API_BASE}/api/cart/items/${cartItemId}/remove/`, axiosConfig);
      const updated = { ...cart };
      delete updated[menuItemId];
      setCart(updated);
      console.log('🗑️ Item removed from cart');
    } catch (err) {
      console.error('❌ Remove failed:', err);
    }
  };

  const handleQuantityChange = async (menuItemId, delta) => {
    const item = cart[menuItemId];
    if (!item || !item.cart_item_id) return;

    const newQuantity = item.quantity + delta;
    if (newQuantity < 1) return;

    try {
      await axios.put(
        `${API_BASE}/api/cart/items/${item.cart_item_id}/update/`,
        { quantity: newQuantity },
        axiosConfig
      );
      setCart({
        ...cart,
        [menuItemId]: { ...item, quantity: newQuantity },
      });
      console.log(`🔄 Quantity updated to ${newQuantity} for ${item.name}`);
    } catch (err) {
      console.error('❌ Failed to update quantity:', err);
    }
  };

  const handlePlaceOrder = async () => {
    if (Object.keys(cart).length === 0) {
      alert('Your cart is empty!');
      return;
    }

    setPlacingOrder(true); // ✅ Start placing

    try {
      const res = await axios.post(
        `${API_BASE}/api/orders/place/`,
        { notes: 'Deliver quickly' },
        axiosConfig
      );

      const { order } = res.data;
      const orderId = `ORD${order.id}`;
      const time = new Date(order.created_at).toLocaleString();

      const items = order.items.map((item) => {
        const cartItem = cart[item.menu_item];
        const price = cartItem?.price ?? 0;

        return {
          name: item.menu_item_name || cartItem?.name || `Item #${item.menu_item}`,
          quantity: item.quantity,
          price,
        };
      });

      const total = parseFloat(order.total_amount);

      if (user?.email) {
        const key = `orderHistory_${user.email}`;
        const prevOrders = JSON.parse(localStorage.getItem(key)) || [];
        const newOrder = { orderId, time, items, total };
        localStorage.setItem(key, JSON.stringify([newOrder, ...prevOrders]));
      }

      setOrderDetails({ orderId, time, items, total });
      setCart({});
      console.log('✅ Order placed successfully:', order);
    } catch (err) {
      console.error('❌ Order placement failed:', err);
      alert('Failed to place order. Please try again.');
    } finally {
      setPlacingOrder(false); // ✅ Done placing
    }
  };

  const cartTotal = Object.values(cart).reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <div className="cart-container">
      <h2>🛒 Your Cart</h2>

      {orderDetails ? (
        <div className="order-confirmation">
          <h3><span style={{ color: '#00c853' }}></span> Your Order Has Been Placed</h3>
          <p><strong>Order ID:</strong> {orderDetails.orderId}</p>
          <p><strong>Time:</strong> {orderDetails.time}</p>
          <ul>
            {orderDetails.items.map((item, index) => (
              <li key={index}>
                {item.name} × {item.quantity} = ₹{(item.price * item.quantity).toFixed(2)}
              </li>
            ))}
          </ul>
          <h4>Total Paid: ₹{orderDetails.total.toFixed(2)}</h4>
        </div>
      ) : Object.keys(cart).length === 0 ? (
        <div className="empty-cart-box">
          <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-JGyBEKsrSjQWZJTJ-B8uNYsOGMbtasr3YA&s" />
          <h3>Your cart is empty 🛒</h3>
          <p>Add some delicious meals 😋</p>
          <button className="explore-btn" onClick={() => navigate('/menu')}>
            Explore Menu
          </button>
        </div>
      ) : (
        <>
          <table className="cart-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Price (₹)</th>
                <th>Quantity</th>
                <th>Subtotal (₹)</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(cart).map(([key, item]) => (
                <tr key={key}>
                  <td>{item.name}</td>
                  <td>{item.price}</td>
                  <td>
                    <button className="qty-btn" onClick={() => handleQuantityChange(item.id, -1)}>-</button>
                    <span className="qty-display">{item.quantity}</span>
                    <button className="qty-btn" onClick={() => handleQuantityChange(item.id, 1)}>+</button>
                  </td>
                  <td>{(item.price * item.quantity).toFixed(2)}</td>
                  <td>
                    <button className="remove-btn" onClick={() => handleRemove(item.id)}>Remove</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="cart-summary">
            <h3>Total: ₹{cartTotal.toFixed(2)}</h3>
            <button
              className="place-order-btn"
              onClick={handlePlaceOrder}
              disabled={placingOrder} // ✅ Disable while placing
            >
              {placingOrder ? 'Placing Order...' : 'Place Order'}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;