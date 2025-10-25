import React, { useEffect, useState } from 'react';
import api from '../../api';
import './Orders.css';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [cancellingOrder, setCancellingOrder] = useState(null);

  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const statusDisplayMap = {
    PLACED: 'Placed',
    CONFIRMED: 'Confirmed',
    PREPARING: 'Preparing',
    READY: 'Ready',
    DELIVERED: 'Delivered',
    CANCELLED: 'Cancelled',
  };

  const fetchOrders = async () => {
    setLoading(true);
    setError('');

    try {
      const { data } = await api.get('/api/orders/');
      const apiOrders = data.results ?? data;

      let unsavedLocal = [];
      if (user?.email) {
        const localKey = `orderHistory_${user.email}`;
        const raw = localStorage.getItem(localKey);
        if (raw) {
          try {
            const parsed = JSON.parse(raw);
            unsavedLocal = parsed.filter((o) => !o.id);
          } catch {
            /* ignore */
          }
        }
      }

      setOrders([...apiOrders, ...unsavedLocal]);
    } catch (e) {
      console.error(e);
      setError('Failed to load order history.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;

    setCancellingOrder(orderId);

    try {
      await api.post(`/api/orders/${orderId}/cancel/`, {});

      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.id === orderId ? { ...order, status: 'CANCELLED' } : order
        )
      );

      if (user?.email) {
        const localKey = `orderHistory_${user.email}`;
        const stored = localStorage.getItem(localKey);
        if (stored) {
          try {
            const localOrders = JSON.parse(stored);
            const updatedLocalOrders = localOrders.map((order) =>
              order.id === orderId ? { ...order, status: 'CANCELLED' } : order
            );
            localStorage.setItem(localKey, JSON.stringify(updatedLocalOrders));
          } catch (err) {
            console.warn('Failed to update local storage:', err);
          }
        }
      }

      alert('Order cancelled successfully!');
    } catch (err) {
      console.error('❌ Failed to cancel order:', err);
      const errorMessage =
        err.response?.data?.error ||
        err.response?.data?.message ||
        'Failed to cancel order. Please try again.';
      alert(errorMessage);
    } finally {
      setCancellingOrder(null);
    }
  };

  const canCancelOrder = (order) => {
    return order.id && !['CANCELLED', 'DELIVERED'].includes(order.status);
  };

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'orders_bump') fetchOrders();
    };
    window.addEventListener('storage', handler);
    return () => window.removeEventListener('storage', handler);
  }, []);

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (err) {
      return 'Invalid Date';
    }
  };

  return (
    <div className="orders-container">
      <h2 className="orders-title">
        Order History
        <button
          onClick={fetchOrders}
          className="refresh-btn"
          style={{
            marginLeft: '20px',
            padding: '5px 15px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Refresh
        </button>
      </h2>

      {loading ? (
        <p>Loading your orders...</p>
      ) : error ? (
        <div style={{ color: 'red' }}>
          {error}
          <button onClick={fetchOrders} style={{ marginLeft: '10px' }}>
            Retry
          </button>
        </div>
      ) : orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <div className="orders-table-wrapper">
          <table className="orders-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Date</th>
                <th>Status</th>
                <th>Items</th>
                <th>Total (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order, orderIndex) => {
                const orderTime = formatDate(order.created_at || order.time);
                const items = (order.items || []).map((item) => {
                  const name =
                    item.menu_item_name ||
                    item.name ||
                    item.menu_item?.name ||
                    `Item #${item.menu_item?.id || 'N/A'}`;
                  const quantity = item.quantity || 1;
                  const price =
                    Number(
                      item.price ??
                        item.menu_item_price ??
                        item.menu_item?.price ??
                        0
                    ) || 0;

                  return {
                    id: item.id || Math.random().toString(36).substr(2, 9), // fallback ID
                    name,
                    quantity,
                    price,
                  };
                });

                const total = Number(
                  order.total || order.total_amount || 0
                ).toFixed(2);
                const orderId = order.orderId || order.id || `local-${orderIndex}`;
                const orderStatus = order.status || 'PLACED';

                return (
                  <tr key={`order-${orderId}`}>
                    <td>#{orderId}</td>
                    <td>{orderTime}</td>
                    <td>
                      <span
                        className={`status-badge status-${orderStatus.toLowerCase()}`}
                      >
                        {statusDisplayMap[orderStatus] || orderStatus}
                      </span>
                    </td>
                    <td>
                      <ul className="order-items-list">
                        {items.map((item, idx) => (
                          <li key={`item-${orderId}-${item.id || idx}`}>
                            {item.name} × {item.quantity} = ₹
                            {(item.price * item.quantity).toFixed(2)}
                          </li>
                        ))}
                      </ul>
                    </td>
                    <td>₹{total}</td>
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
                            cursor:
                              cancellingOrder === order.id
                                ? 'not-allowed'
                                : 'pointer',
                          }}
                        >
                          {cancellingOrder === order.id
                            ? 'Cancelling...'
                            : 'Cancel Order'}
                        </button>
                      ) : (
                        <span className="no-action" style={{ color: '#666' }}>
                          {orderStatus === 'CANCELLED'
                            ? 'Cancelled'
                            : orderStatus === 'DELIVERED'
                            ? 'Delivered'
                            : !order.id
                            ? 'Local Order'
                            : 'Cannot Cancel'}
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Orders;
