import React, { useState, useEffect } from 'react';
import './Orders.css';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const getAdminToken = () => {
    const token = localStorage.getItem('adminToken');
    console.log('Orders - Token:', token);
    return token;
  };

  const fetchOrders = async () => {
    setLoading(true);
    setError('');

    try {
      const token = getAdminToken();
      if (!token) {
        setError('No admin access token found. Please login again.');
        return;
      }

      const res = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/orders/admin/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        const data = await res.json();
        setOrders(data.results || data);
      } else {
        setError('Failed to fetch orders');
      }
    } catch (err) {
      console.error(err);
      setError('Network error. Please check your connection.');
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