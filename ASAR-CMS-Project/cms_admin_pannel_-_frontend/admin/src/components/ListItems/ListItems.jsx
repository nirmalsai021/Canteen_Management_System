import React, { useState, useEffect } from 'react';
import './ListItems.css';

const ListItems = ({ onUpdateMenuItem, onDeleteMenuItem }) => {
  /* ─────────── State ─────────── */
  const [menuItems, setMenuItems] = useState([]);
  const [editIndex, setEditIndex] = useState(null);
  const [editedItem, setEditedItem] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  /* ─────────── Constants ─────────── */
  const categoryOptions = [
    { display: 'Breakfast', value: 'breakfast' },
    { display: 'Lunch',     value: 'lunch'     },
    { display: 'Drinks',    value: 'drinks'    },
    { display: 'Snacks',    value: 'snacks'    },
    { display: 'Juices',    value: 'juices'    },
  ];

  const getAdminToken = () =>
    localStorage.getItem('admin_access_token') ||
    localStorage.getItem('access_token');

  /* ─────────── Data fetch ─────────── */
  const fetchMenuItems = async () => {
    setIsLoading(true);
    setError('');

    try {
      const token = getAdminToken();
      if (!token) {
        setError('No admin access token found. Please login again.');
        return;
      }

      const res = await fetch('http://localhost:8000/api/menu/admin/', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        setMenuItems(await res.json());
      } else if (res.status === 401) {
        setError('Unauthorized. Please login again.');
        localStorage.clear();
      } else if (res.status === 403) {
        setError('Forbidden. Admin access required.');
      } else {
        const err = await res.json().catch(() => ({}));
        setError(err.error || `Failed to fetch menu items (${res.status})`);
      }
    } catch (err) {
      console.error(err);
      setError('Network error. Please check your connection.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchMenuItems(); }, []);

  /* ─────────── Edit handlers ─────────── */
  const handleEdit = (index) => {
    setEditIndex(index);
    setEditedItem({ ...menuItems[index] }); // clone to avoid mutation
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedItem(prev => {
      switch (name) {
        case 'available': return { ...prev, available: value === 'true' };
        case 'price':     return { ...prev, price: value };  // keep string
        default:          return { ...prev, [name]: value };
      }
    });
  };

  const cancelEdit = () => {
    setEditIndex(null);
    setEditedItem({});
  };

  const saveEdit = async () => {
    /* basic front-end validation */
    if (!editedItem.name?.trim()) {
      alert('Item name is required'); return;
    }
    if (editedItem.price === '' || isNaN(+editedItem.price)) {
      alert('Price must be a valid number'); return;
    }
    if (!editedItem.category) {
      alert('Please select a category'); return;
    }

    const token = getAdminToken();
    if (!token) { alert('No admin token. Please login again.'); return; }

    /* ── build payload ── */
    const img = editedItem.image?.trim();
    const payload = {
      name:        editedItem.name.trim(),
      description: editedItem.description?.trim() || '',
      price:       parseFloat(editedItem.price),
      available:   editedItem.available,
      category:    editedItem.category,
      // image will be conditionally added below
    };

    /* Only include image when it's NOT an external URL and not empty */
    if (img && !img.startsWith('http')) {
      payload.image = img;          // e.g. "menu_images/foo.jpg"
    }
    /* If img is blank or an external URL, omit the key entirely */

    try {
      const res = await fetch(
        `http://localhost:8000/api/menu/admin/${menuItems[editIndex].id}/`,
        {
          method: 'PUT',                       // DRF-friendly
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        },
      );

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        console.error('DRF-error payload →', errJson);
        const msg = Object.entries(errJson).length
          ? Object.entries(errJson)
              .map(([f, m]) => `${f}: ${Array.isArray(m) ? m.join(', ') : m}`)
              .join('\n')
          : `HTTP ${res.status}`;
        alert(`Update failed:\n${msg}`);
        return;
      }

      const updated = await res.json();
      setMenuItems(prev => {
        const next = [...prev];
        next[editIndex] = updated;
        return next;
      });

      setEditIndex(null);
      setEditedItem({});
      onUpdateMenuItem?.(editIndex, updated);
      alert('Menu item updated successfully!');
    } catch (err) {
      console.error(err);
      alert(`Update failed: ${err.message}`);
    }
  };

  /* ─────────── Delete ─────────── */
  const handleDelete = async (index) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    const token = getAdminToken();
    if (!token) { alert('No admin token. Please login again.'); return; }

    try {
      const res = await fetch(
        `http://localhost:8000/api/menu/admin/${menuItems[index].id}/`,
        { method: 'DELETE', headers: { Authorization: `Bearer ${token}` } },
      );

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || err.detail || `HTTP ${res.status}`);
      }

      setMenuItems(prev => prev.filter((_, i) => i !== index));
      onDeleteMenuItem?.(index);
      alert('Menu item deleted successfully!');
    } catch (err) {
      console.error(err);
      alert(`Delete failed: ${err.message}`);
    }
  };

  /* ─────────── Helpers ─────────── */
  const getCategoryDisplay = (val) =>
    categoryOptions.find(opt => opt.value === val)?.display || val;

  const getImageUrl = (path) => {
    if (!path) return null;
    return path.startsWith('http')
      ? path
      : `http://localhost:8000${path.startsWith('/') ? '' : '/'}${path}`;
  };

  /* ─────────── Render ─────────── */
  if (isLoading) {
    return (
      <div className="list-items-container">
        <div className="loading">Loading menu items...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="list-items-container">
        <div className="error-message">
          {error}
          <button onClick={fetchMenuItems} style={{ marginLeft: '10px' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="list-items-container">
      <div className="table-wrapper">
        <div className="header-section">
          <h2>All Menu Items</h2>
          <button className="refresh-btn" onClick={fetchMenuItems}>
            Refresh
          </button>
        </div>

        {menuItems.length === 0 ? (
          <p>No items available. Please add some menu items.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Description</th>
                <th>Price (₹)</th>
                <th>Availability</th>
                <th>Category</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {menuItems.map((item, index) => (
                <tr key={item.id ?? index}>
                  {editIndex === index ? (
                    /* ────── Edit row ────── */
                    <>
                      <td>
                        <div className="image-edit-container">
                          {editedItem.image && (
                            <img
                              src={getImageUrl(editedItem.image)}
                              alt={editedItem.name}
                              className="menu-item-image-small"
                              onError={e => (e.target.style.display = 'none')}
                            />
                          )}
                          <input
                            name="image"
                            value={editedItem.image || ''}
                            onChange={handleChange}
                            placeholder="Image URL or leave blank"
                            className="image-input"
                          />
                        </div>
                      </td>

                      <td>
                        <input
                          name="name"
                          value={editedItem.name || ''}
                          onChange={handleChange}
                          required
                          placeholder="Enter item name"
                        />
                      </td>

                      <td>
                        <textarea
                          name="description"
                          value={editedItem.description || ''}
                          onChange={handleChange}
                          placeholder="Enter description (optional)"
                          rows="2"
                        />
                      </td>

                      <td>
                        <input
                          name="price"
                          type="number"
                          step="0.01"
                          min="0"
                          value={editedItem.price || ''}
                          onChange={handleChange}
                          required
                          placeholder="0.00"
                        />
                      </td>

                      <td>
                        <select
                          name="available"
                          value={editedItem.available ? 'true' : 'false'}
                          onChange={handleChange}
                        >
                          <option value="true">Available</option>
                          <option value="false">Not Available</option>
                        </select>
                      </td>

                      <td>
                        <select
                          name="category"
                          value={editedItem.category || ''}
                          onChange={handleChange}
                          required
                        >
                          <option value="">Select Category</option>
                          {categoryOptions.map(opt => (
                            <option key={opt.value} value={opt.value}>
                              {opt.display}
                            </option>
                          ))}
                        </select>
                      </td>

                      <td>
                        <button className="edit-btn"   onClick={saveEdit}>Save</button>
                        <button className="cancel-btn" onClick={cancelEdit}>Cancel</button>
                      </td>
                    </>
                  ) : (
                    /* ────── Read-only row ────── */
                    <>
                      <td>
                        <div className="image-container">
                          {getImageUrl(item.image) ? (
                            <img
                              src={getImageUrl(item.image)}
                              alt={item.name}
                              className="menu-item-image-small"
                              onError={e => {
                                e.target.src = '/api/placeholder/50/50';
                                e.target.alt = 'No image';
                              }}
                            />
                          ) : (
                            <div className="no-image-placeholder">No Image</div>
                          )}
                        </div>
                      </td>

                      <td>{item.name}</td>
                      <td>{item.description || 'No description'}</td>
                      <td>₹{parseFloat(item.price).toFixed(2)}</td>

                      <td>
                        <span
                          className={`availability ${
                            item.available ? 'in-stock' : 'out-of-stock'
                          }`}
                        >
                          {item.available ? 'Available' : 'Not Available'}
                        </span>
                      </td>

                      <td>{getCategoryDisplay(item.category)}</td>

                      <td>
                        <button className="edit-btn"   onClick={() => handleEdit(index)}>Edit</button>
                        <button className="delete-btn" onClick={() => handleDelete(index)}>Delete</button>
                      </td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default ListItems;