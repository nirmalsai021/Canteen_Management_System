import React, { useState, useEffect } from 'react';
import './Orders.css';
import api from '../../api';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [cancellingOrder, setCancellingOrder] = useState(null);

  const fetchOrders = async () => {
    setLoading(true);
    setError('');

    try {
      console.log('Fetching orders...');
      const token = localStorage.getItem('admin-token');
      console.log('Token for orders:', token);
      
      // Use the configured API instance which handles authentication
      const response = await api.get('/api/orders/admin/');
      console.log('Orders response:', response.data);
      setOrders(response.data.results || response.data || []);
    } catch (err) {
      console.error('Error fetching orders:', err);
      console.error('Error response:', err.response);
      // Fallback to empty orders on network error
      setOrders([]);
      setError('Unable to fetch orders. Check network connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;

    setCancellingOrder(orderId);

    try {
      await api.post(`/api/orders/${orderId}/cancel/`);
      
      // Update order status in local state
      setOrders(prevOrders =>
        prevOrders.map(order =>
          order.id === orderId ? { ...order, status: 'CANCELLED' } : order
        )
      );

      alert('Order cancelled successfully!');
    } catch (err) {
      console.error('❌ Failed to cancel order:', err);
      const errorMessage = err.response?.data?.error || err.response?.data?.debug || 'Failed to cancel order. Please try again.';
      
      // If order was actually cancelled (status 200 but error in response), refresh the list
      if (err.response?.status === 200 || errorMessage.includes('successfully')) {
        fetchOrders(); // Refresh to show updated status
        alert('Order cancelled successfully!');
      } else {
        alert(`Error: ${errorMessage}`);
      }
    } finally {
      setCancellingOrder(null);
    }
  };

  const canCancelOrder = (order) => {
    return !['CANCELLED', 'DELIVERED'].includes(order.status);
  };

  useEffect(() => {
    fetchOrders();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

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
              <th>Actions</th>
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
                <td>
                  <span className={`status-badge status-${order.status.toLowerCase()}`}>
                    {order.status}
                  </span>
                </td>
                <td>{new Date(order.created_at).toLocaleDateString()}</td>
                <td>
                  {canCancelOrder(order) ? (
                    <button
                      className="cancel-btn"
                      onClick={() => handleCancelOrder(order.id)}
                      disabled={cancellingOrder === order.id}
                      style={{
                        backgroundColor: '#dc3545',
                        color: 'white',
                        border: 'none',
                        padding: '5px 10px',
                        borderRadius: '4px',
                        cursor: cancellingOrder === order.id ? 'not-allowed' : 'pointer'
                      }}
                    >
                      {cancellingOrder === order.id ? 'Cancelling...' : 'Cancel Order'}
                    </button>
                  ) : (
                    <span style={{ color: '#666' }}>
                      {order.status === 'CANCELLED' ? 'Cancelled' : 'Cannot Cancel'}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Orders;