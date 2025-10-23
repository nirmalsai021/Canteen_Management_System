import React, { useState } from 'react';
import './AddMenu.css';
import { tokenUtils } from '../../utils/tokenUtils';

const AddMenu = ({ onAddMenuItem }) => {
  const [menuItem, setMenuItem] = useState({
    name: '',
    description: '',
    price: '',
    available: true,
    category: 'snacks', // Default to 'snacks' as per API
  });
  
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Category options based on API documentation
  const categoryOptions = [
  { display: 'Breakfast', value: 'breakfast' },
  { display: 'Lunch', value: 'lunch' },
  { display: 'Drinks', value: 'drinks' },
  { display: 'Snacks', value: 'snacks' }
];


  // Get admin token using centralized utility
  const getAdminToken = () => {
    return tokenUtils.getToken();
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'available') {
      setMenuItem({ ...menuItem, [name]: value === 'true' });
    } else {
      setMenuItem({ ...menuItem, [name]: value });
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        setError('Please select a valid image file (JPEG, PNG, or GIF)');
        return;
      }
      
      // Validate file size (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) {
        setError('Image file size should be less than 5MB');
        return;
      }

      setImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // FIXED: Use the helper function to get admin token
      const token = getAdminToken();
      
      if (!token) {
        throw new Error('Admin authentication required. Please login again.');
      }

      // Validate required fields
      if (!menuItem.name.trim()) {
        throw new Error('Menu item name is required');
      }
      
      if (!menuItem.price || parseFloat(menuItem.price) <= 0) {
        throw new Error('Valid price is required');
      }

      let response;

      const headers = {};
      if (token) {
        headers.Authorization = `Token ${token}`;
      }

      if (image) {
        // Use FormData for image upload
        const formData = new FormData();
        formData.append('name', menuItem.name.trim());
        formData.append('description', menuItem.description.trim());
        formData.append('price', parseFloat(menuItem.price).toFixed(2));
        formData.append('available', menuItem.available);
        formData.append('category', menuItem.category);
        formData.append('image', image);

        response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/menu/add/`, {
          method: 'POST',
          headers,
          body: formData
        });
      } else {
        // Use JSON for text-only data
        const payload = {
          name: menuItem.name.trim(),
          description: menuItem.description.trim(),
          price: parseFloat(menuItem.price).toFixed(2),
          available: menuItem.available,
          category: menuItem.category
        };

        response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/menu/add/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...headers
          },
          body: JSON.stringify(payload)
        });
      }

      if (!response.ok) {
        // Handle different error types
        if (response.status === 401) {
          throw new Error('Unauthorized. Please login again.');
        } else if (response.status === 403) {
          throw new Error('Forbidden. Admin access required.');
        } else if (response.status === 400) {
          const errorData = await response.json();
          
          // Format validation errors
          let errorMessage = 'Validation errors:\n';
          Object.keys(errorData).forEach(field => {
            if (Array.isArray(errorData[field])) {
              errorMessage += `${field}: ${errorData[field].join(', ')}\n`;
            } else {
              errorMessage += `${field}: ${errorData[field]}\n`;
            }
          });
          
          throw new Error(errorMessage);
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      const data = await response.json();
      
      // Success - call parent callback if provided
      if (onAddMenuItem) {
        onAddMenuItem(data);
      }

      setSuccess('Menu item added successfully!');
      
      // Reset form
      setMenuItem({
        name: '',
        description: '',
        price: '',
        available: true,
        category: 'snacks',
      });
      setImage(null);
      setImagePreview(null);
      
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = '';
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="menu-form-container">
      <h2>Add Menu Item</h2>
      
      {error && (
        <div className="error-message" style={{ 
          color: 'red', 
          marginBottom: '10px', 
          padding: '10px', 
          backgroundColor: '#ffebee', 
          border: '1px solid #f44336',
          borderRadius: '4px',
          whiteSpace: 'pre-line'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {success && (
        <div className="success-message" style={{ 
          color: 'green', 
          marginBottom: '10px', 
          padding: '10px', 
          backgroundColor: '#e8f5e8', 
          border: '1px solid #4caf50',
          borderRadius: '4px'
        }}>
          <strong>Success:</strong> {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Food Item Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            placeholder="Enter food item name"
            value={menuItem.name}
            onChange={handleChange}
            required
            disabled={loading}
            maxLength={100}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            placeholder="Enter item description (optional)"
            value={menuItem.description}
            onChange={handleChange}
            disabled={loading}
            rows={3}
          />
        </div>

        <div className="form-group">
          <label htmlFor="price">Price (₹) *</label>
          <input
            type="number"
            id="price"
            name="price"
            placeholder="Enter price"
            value={menuItem.price}
            onChange={handleChange}
            step="0.01"
            min="0"
            max="9999.99"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="available">Availability</label>
          <select 
            id="available"
            name="available" 
            value={menuItem.available.toString()} 
            onChange={handleChange}
            disabled={loading}
          >
            <option value="true">Available</option>
            <option value="false">Not Available</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="category">Category *</label>
          <select 
            id="category"
            name="category" 
            value={menuItem.category} 
            onChange={handleChange}
            disabled={loading}
            required
          >
            {categoryOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.display}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="image">Item Image</label>
          <input
            type="file"
            id="image"
            name="image"
            accept="image/*"
            onChange={handleImageChange}
            disabled={loading}
          />
          <small style={{ color: '#666', fontSize: '0.9em' }}>
            Optional. Accepted formats: JPEG, PNG, GIF. Max size: 5MB
          </small>
        </div>

        {imagePreview && (
          <div className="image-preview" style={{ marginBottom: '15px' }}>
            <label>Image Preview:</label>
            <img 
              src={imagePreview} 
              alt="Preview" 
              style={{ 
                maxWidth: '200px', 
                maxHeight: '200px', 
                display: 'block', 
                marginTop: '5px',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }} 
            />
          </div>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Menu Item'}
        </button>
      </form>
    </div>
  );
};

export default AddMenu;