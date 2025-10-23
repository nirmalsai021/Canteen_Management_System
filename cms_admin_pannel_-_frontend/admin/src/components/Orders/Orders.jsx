import React, { useState, useEffect } from 'react';
import './Orders.css';
import { tokenUtils } from '../../utils/tokenUtils';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const getAdminToken = () => {
    return tokenUtils.getToken();
  };

  const fetchOrders = async () => {
    setLoading(true);
    setError('');

    try {
      const token = getAdminToken();
      const headers = {};
      if (token) {
        headers.Authorization = `Token ${token}`;
      }
      
      // Try to fetch real orders from backend
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/orders/admin/`, { headers });
      
      if (res.ok) {
        const data = await res.json();
        setOrders(data.results || data || []);
      } else {
        // Fallback to empty orders if endpoint requires auth
        setOrders([]);
        setError('No orders available or authentication required.');
      }
    } catch (err) {
      // Fallback to empty orders on network error
      setOrders([]);
      setError('Unable to fetch orders. Check network connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  if (loading) return <div>Loading orders...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="orders-container">
      <h2>Customer Orders</h2>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <table className="orders-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Total</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{order.user?.username || 'Unknown'}</td>
                <td>
                  {order.items?.map((item, idx) => (
                    <div key={idx}>
                      {item.menu_item_name} x{item.quantity}
                    </div>
                  ))}
                </td>
                <td>₹{parseFloat(order.total_amount || 0).toFixed(2)}</td>
                <td>{order.status}</td>
                <td>{new Date(order.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Orders;